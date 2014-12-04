#!/usr/bin/env python

import sys
from TwitterAPI import TwitterAPI

from TwitterMySQL import TwitterMySQL
print "Using " + str(sys.modules['TwitterMySQL'])

##### PARAMS TO EDIT
twitter_cred_filename = "twitterapi_credentials.txt"
server = "wwbp"
db = "selah"
table = "allGeotagsStreamed"
#####


##read credentials and set up API
with open(twitter_cred_filename, "r") as f:
    (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET) = [line.split("=")[1].strip() for line in f]

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)

mysql_columns_exp = ["user_id bigint(20)", "message_id bigint(20) primary key", "message text", "created_time datetime",
                     "in_reply_to_message_id bigint(20)", "in_reply_to_user_id bigint(20)",
                     "source varchar(128)", "lang varchar(4)", "time_zone varchar(64)",
                     "user_location varchar(128)", "tweet_location varchar(128)", "coordinates varchar(128)",
                     "coordinates_address varchar(64)", "coordinates_state varchar(3)", "index userindex (user_id)"]


twtSQL = TwitterMySQL(db=db, host=server, api=api, SQLfieldsExp = mysql_columns_exp, table=table, dropIfExists = True, charset='utf8', use_unicode = True)
##this is a streaming API request
##this coordinate box covers most of the USA and Canada
twtSQL.tweetsToMySQL("statuses/filter", locations='-161, 17, -57, 65')
















