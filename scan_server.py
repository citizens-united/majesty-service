#!/usr/bin/env python3
# Respond to requests for scans
# http://docs.tweepy.org/en/v3.6.0/api.html

import tweepy
import time
import re
import sys
import random

from trollbot_support_lib import *

# set before launch
MY_USERNAME = '@YourUsernameHere'

LAST_REQUEST_FILENAME = 'last_request_responded_to.txt'


def set_last_request_responded_to(tweet_id):
    ''' sets id to last_request_responded_to.txt
    '''
    with open(LAST_REQUEST_FILENAME,'w',encoding = 'utf-8') as f:
        f.write(str(tweet_id))


def get_last_request_responded_to():
    ''' gets id from last_request_responded_to.txt
    '''
    with open(LAST_REQUEST_FILENAME,'r',encoding = 'utf-8') as f:
        return f.readline()


def get_link_to_trollbot_links(trollbots):
    ''' TODO pastes on a site like rentry.co and returns link
    '''
    # return link_to_trollbot_links
    pass
    

def compose_reply_tweet(requestor_username, target_username, trollbots):
    ''' TODO: should be more varied
    '''
    
    count = len(trollbots)

    tweet = '@' + requestor_username + ' ' 
    tweet = tweet + target_username + " followed by ≥" + str(count) + " trollbots:\n" 
    tweet = tweet + get_human_readable_list_of_users(trollbots)

    # we want to give them a broad range of the available trollbots, rather than skim some off the top. TODO: should cache them and support requests for "more"
    random.shuffle(trollbots)

    hit_limit = False

    while len(tweet) > TWEET_CHAR_LIMIT - 10:

        hit_limit = True

        # Remove the last token
        tweet = tweet.split(' ')
        tweet = tweet[:-1]
        tweet = ' '.join(tweet)

    if hit_limit:
        tweet = tweet + ' and more'

    if count == 0:
        tweet = '@' + requestor_username + ' ' 
        tweet = tweet + 'detected no trollbots following ' + target_username + '. Good, but remain vigilant.'

    print("composed tweet:\n" + tweet)

    return tweet
    

def post_reply_tweet(api, username, reply_tweet, tweet_id):
    ''' 
    '''

    api.update_status(reply_tweet, tweet_id)
    

def respond_to_scan_request(api, mention):
    ''' Scans requested user and replies
    '''

    print('Responding to scan request: ' + str(mention.text))

    # if the request is coming from a trollbot, ignore it
    if is_trollbot(api, mention.user):
        return

    #import pdb; pdb.set_trace()

    # extract the username to scan from the mention
    username = extract_username(mention, MY_USERNAME)

    # find the trollbots,
    try:
        # sometimes fails with tweepy.error.TweepError: Not authorized.
        trollbots = scan_user(api, username)

    except tweepy.error.TweepError:
        # will try again anyway
        print("probably blocked please check")
        return

    # report them,
    report_trollbots(api, trollbots)

    # TODO: paste them on rentry.co or something @someday
    #link_to_trollbot_links = get_link_to_trollbot_links(trollbots)

    # compose reply tweet
    reply_tweet = compose_reply_tweet(mention.user.screen_name, username, trollbots)

    # post reply tweet
    post_reply_tweet(api, mention.user.screen_name, reply_tweet, mention.id)

    # set last_request_responded_to.txt
    set_last_request_responded_to(mention.id)


def is_request(text):
    ''' examines the text for 'scan' and a username or 'me'
    '''

    # if they said "scan..."
    if 'scan' in text.lower():

        # check for usernames
        usernames = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', text)

        if len(usernames) != 0:
            return True

        # check for "me"
        if 'me' in text.lower():
            return True

    return False


def check_for_scan_requests(api):
    ''' Checks mentions for scan requests and returns a list of them.
    '''

    last_request_responded_to = get_last_request_responded_to()

    print("last request responded to: " + last_request_responded_to)

    try:
        # sometimes this fails with connection aborted
        mentions = api.mentions_timeline(since_id=last_request_responded_to, count=20)

    except:
        # will try again anyway
        return []

    # a list of requests to scan users
    requests = []

    for mention in mentions:

        # remove mention of myself from the text
        text = mention.text.replace(MY_USERNAME, '')

        if is_request(text):
            requests.append(mention)

    return requests


def main_loop():
    ''' Spins, responding to requests.
    '''
    api = get_api()
    print(api.me().screen_name)

    print('Find and report trollbots upon request.')
    print('May be slow; Twitter allows 15 API calls per 15 minutes.')

    #followers_processed = 0
    #trollbots_found = 0
    #batchNumber = 1
    count = 0

    while(True):
        count = count + 1
        print('sleeping 10 seconds...' + str(count))
        time.sleep(10)

        requests = check_for_scan_requests(api)

        for request in requests:
            respond_to_scan_request(api, request)


if __name__ == "__main__":
    main_loop()
