#!/usr/bin/env python

import sys
from TwitterMySQL import TwitterMySQL
from TwitterAPI import TwitterAPI

##### PARAMS TO EDIT
twitter_cred_filename = "twitterapi_credentials.txt"
server = "wwbp"
db = "selah"
#####

##read credentials and set up API
with open(twitter_cred_filename, "r") as f:
    (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET) = [line.split("=")[1].strip() for line in f]

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

screen_name = sys.argv[1]
table_name = sys.argv[2]
assert sys.argv[1] and sys.argv[2], "Useage: tweetsToDB.py <screenName> <tableName>"

print screen_name + " " + table_name

#NOTE - created_time must be in fourth column or else there will be errors due to bug
mysql_columns = ["user_id bigint(20)",
                 "message_id bigint(20) primary key",
                 "message text",
                 "created_time datetime",
                 "screen_name varchar(128)"]

jTweetToRow = {
    'message_id': "['id_str']",
    'screen_name': "['user']['screen_name']",
    'message': "['text']",
    'user_id': "['user']['id_str']",
    'created_time': "['created_at']"
}

#I believe column definition and JTweet to row must be comprehensive, it does not just add to the defaults
twtSQL = TwitterMySQL(api=api, host=server, db=db, table=table_name,
                                   SQLfieldsExp=mysql_columns, jTweetToRow=jTweetToRow)

#I believe I cannot put column definition or JTweetToRow down here
twtSQL.userTimelineToMySQL(screen_name=screen_name)
