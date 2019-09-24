# Find the bots following a hardcoded list of users and report them
# http://docs.tweepy.org/en/v3.6.0/api.html

import tweepy
import time
import re
import random
import trollbot_support_lib as tsl

print('Find the bots on a hardcoded list and report them.')
print('Allow this to run for a long time; Twitter allows 15 API calls per 15 minutes.')

# these are the seeds
suspects = [ '@karen_storer','@johnbro70166708', '@SlovadonVinavic' ,'@eileenr68427662','@prettybird450', '@DoxianaT', '@SusanHaymon1','@dewaynehines66', '@polcatron','@Conny_Servative', '@golfingbynoon','@margaret9449','@nathansthepilot', '@ran_hinrichs', '@DebiDkruse','@raelynne1993','@howardmood449', '@sinisteracosta', '@OregonMuse', '@ChellisNancy','@SFCArmyWifeMN', '@ColetteIBryant','@CjonesCar', '@UTAH744','@The__Snowman', '@mkfitness1', '@tonibaloney619','@Skyblade12','@pmcsupertuners','@rushsylvania', '@RealDan0mite', '@horsemodels', '@TiredOfThieves', '@redrockredrock', '@DanAuito', '@williamlharbuck', '@DeniseRapp1', '@realDonaldTrump', '@GenFlynn', '@RitaCosby', '@AntonioSabatoJr', '@darkom56', '@LolaBahadourian', '@tam1lap', '@battleofever', '@genflynn', '@Mama_O_G', '@THEHermanCain', '@GenFlynn', '@BrandonStraka', '@RealJack', '@RealOmarNavarro', '@Education4Libs', '@RyanAFournier', '@1USANationalist', '@NancyOB49582905', '@nanc_eeeee', '@ThierryMotyLoic', '@deviceproblem', '@Lothaletrom67', '@Douglash55', '@Murphy931339211', '@Calif_Lew', '@RealitySmackU', '@We_AreAlert', '@LfodtP', '@ConservativeXT', '@GenFlynn', '@hubcitymn', '@christian144Han', '@rgividen', '@mlhcromwell16', '@TheEvaRoyer', '@retirewcashflow', '@AlbertoStorelli', '@QuiltersArk', '@MAGA', '@KAG', '@POTUS', '@QArmy1777', '@liberaltears67']

api = tsl.get_api()

for suspect_name in suspects:
    print("scanning www.twitter.com/" + suspect_name + " ...")
    api = tsl.deep_scan_suspect(api, suspect_name)
    
print('Done.')
