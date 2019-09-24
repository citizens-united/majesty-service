''' lots of functions that can be reused for trollbot seek and destroy tasks
'''

import re
import tweepy

# I think the reporting limit is 49 per day or something, not sure.
#REPORTING_LIMIT = 49
TWEET_CHAR_LIMIT = 280

# Sample some accounts and set these to taste
MAX_FOLLOWERS = 2
#MAX_FOLLOWING = 20
MAX_TWEETS = 2
TWEETS_PER_FOLLOWER_THRESHOLD = 50

# this can be higher than actual number of followers and it does not crash.
NUM_FOLLOWERS_TO_EXAMINE = 200
MAX_BOTS_PER_SCAN = 15

def get_api():
        # The API handle for a good british guardbotte
        consumerkey = 'get'
        consumersecret = 'your'
        accesstoken = 'own'
        accesstokensecret = 'keys'
        
        auth = tweepy.OAuthHandler(consumerkey, consumersecret)
        auth.set_access_token(accesstoken, accesstokensecret)
        api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        return api


def get_human_readable_list_of_users(users):
    text = ''

    for user in users:
        text = text +  '@' + user.screen_name + ' '

    return text


def is_trollbot(api, suspect):

    # Get their screen name
    screenName = suspect.screen_name
    print("Examining @" + screenName + "...")

    # Does their screen name end with 7 or more numbers? dead givaway
    hasBotName = re.search(r'(\d{7}$)', screenName) != None
    if hasBotName:
        return True

    # get number of connections
    num_followers = suspect.followers_count

    # get the number of tweets they have tweeted
    num_tweets = suspect.statuses_count

    # avoid division by zero
    if num_followers == 0:
        num_followers = 1

    # Check to see if there are too many tweets per follower
    tweets_per_follower = float(num_tweets) / float(num_followers)
    tweets_per_follower = tweets_per_follower > TWEETS_PER_FOLLOWER_THRESHOLD

    # they haven't set a background image
    noBackgroundImage = suspect.profile_background_image_url == None

    # also want profile pic 
    suspectIsSpammer =  tweets_per_follower and noBackgroundImage

    return suspectIsSpammer


def try_to_report(api, suspect):
    ''' Tries to report a user. There is a daily reporting limit, but if you 
        hit it, you'll be fine. Returns a handle to the API.
    '''

    try:
        print("Reporting: twitter.com/" + suspect.screen_name)
        api.report_spam(suspect.id_str)

    except:
        api = get_api()
        
    return api


def report_trollbots(api, trollbots):
    ''' Accepts a list of trollbot user objects and reports them. Returns a handle to the API.
    '''

    for trollbot in trollbots:
        api = try_to_report(api, trollbot)

    return api


def scan_user(api, username):
    ''' Scans a users' followers. Returns a list of suspected trollbots.
    '''

    print("\nScanning " + username + " for trollbots...")

    trollbots = []

    # for follower in followers:
    for follower in tweepy.Cursor(api.followers, screen_name=username, count=NUM_FOLLOWERS_TO_EXAMINE).items():
        
        # If so, append them to the list of trollbots.
        if is_trollbot(api, follower):
            trollbots.append(follower)
            print("trollbot detected: www.twitter.com/" + follower.screen_name)

            # TODO if you ever post to pastebin or whatever automatically, remove this
            if len(trollbots) > MAX_BOTS_PER_SCAN:
                break

    return trollbots


def deep_scan_suspect(api, username):
    ''' Scans a user and their followers.
    '''

    suspect = api.get_user(username)

    if is_trollbot(api, suspect):
        
        api = try_to_report(suspect, api)

        # then scan their followers
        for follower in api.followers(username):

            if is_trollbot(api, follower):
                api = try_to_report(follower, api)

    return api


def extract_username(mention, username):
    ''' Extracts the username from a mention. First priority: The first username that is *not*
        the sender. Second priority: The sender.
    '''

    # remove mention of myself from the text
    text = mention.text.lower().replace(username.lower(), '')

    usernames = re.findall(r'(?<=^|(?<=[^a-zA-Z0-9-_\.]))@([A-Za-z]+[A-Za-z0-9-_]+)', text)

    # if they provided one or more usernames, go with the first one 
    if len(usernames) != 0:
        return usernames[0]

    # otherwise, go with their username
    return mention.user.screen_name

