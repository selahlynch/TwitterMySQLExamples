#!/usr/bin/env python

import sys

from TwitterMySQL import TwitterMySQL
from TwitterAPI import TwitterAPI

import json

assert sys.argv[1] and sys.argv[2], "Useage: tweetsToDB.py <jsonFile> <tableName>"

json_data_file_name = sys.argv[1]
table_name = sys.argv[2]

##### PARAMS TO EDIT
twitter_cred_filename = "twitterapi_credentials.txt"
server = "wwbp"
db = "selah"
#####


#in order to use, must add a directory from the PERMA codeset to the path
sys.path.append("/home/selah/Code/PERMA/data/twitter")
import locationInfo
lm = locationInfo.LocationMap()

##read credentials and set up API
with open(twitter_cred_filename, "r") as f:
    (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET) = [line.split("=")[1].strip() for line in f]

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)



#TODO - edit this
#key - mySQL column name
#value - path to JSON value
jTweetToRow = {
    'id': "['tweet']['id']", #OK
    'message_id': "['tweet']['id']", #OK
    'message': "['tweet']['text']", #OK
    'created_time': "['tweet']['created_at']", #OK
    'user_id': "['tweet']['user']['id']",  #OK
    'in_reply_to_message_id': "['tweet']['in_reply_to_status_id_str']", #OK
    'in_reply_to_user_id': "['tweet']['in_reply_to_user_id_str']", #OK
    'retweet_message_id': "['tweet']['retweet_id']",
    'user_location': "['tweet']['user']['location']", #OK
    'tweet_location': "['tweet']['place']['full_name']",
    'friend_count': "['tweet']['user']['friends_count']",
    'followers_count': "['tweet']['user']['followers_count']",
    'user_time_zone': "['tweet']['user']['time_zone']",
    'lang': "['tweet']['user']['lang']",
    'source': "['tweet']['source']",
    }

mysql_columns = [
    "user_id bigint(20)",
    "message_id bigint(20) primary key",
    "message text",
    "created_time datetime",
    "in_reply_to_message_id bigint(20)",
    "in_reply_to_user_id bigint(20)",
    "retweet_message_id bigint(20)",
    "source varchar(128)",
    "lang varchar(4)",
    "friend_count int(6)",
    "followers_count int(6)",
    "index useriddex (user_id)"]

twtSQL = TwitterMySQL(db=db, host=server, api=api, SQLfieldsExp=mysql_columns,
                                   table=table_name, geoLocate=lm.reverseGeocodeLocal, dropIfExists=True, jTweetToRow=jTweetToRow)

json_data_file = open(json_data_file_name)
json_data = json.load(json_data_file)

tweet_count = 0
for tweet in json_data:

    tweet_count += 1
    if tweet_count % 100 == 0:
        print str(tweet_count) + " tweets counted"

    new_row = twtSQL._prepTweet(tweet)
    twtSQL.insertRows([new_row], verbose=False)







