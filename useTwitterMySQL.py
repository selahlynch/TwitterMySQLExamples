#!/usr/bin/env python

import sys

from TwitterMySQL import TwitterMySQL
from TwitterAPI import TwitterAPI

##### PARAMS TO EDIT
twitter_cred_filename = "twitterapi_credentials.txt"
#####


#in order to use, must add a directory from the PERMA codeset to the path
sys.path.append("/home/selah/Code/PERMA/data/twitter")
import locationInfo
lm = locationInfo.LocationMap()

##read credentials and set up API
with open(twitter_cred_filename, "r") as f:
    (API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET) = [line.split("=")[1].strip() for line in f]

api = TwitterAPI(API_KEY, API_SECRET, ACCESS_TOKEN, ACCESS_SECRET)


mysql_columns = ["user_id", "message_id", "message", "created_time", "in_reply_to_message_id", "in_reply_to_user_id", "retweet_message_id", "source", "lang", "time_zone", "friend_count", "followers_count", "coordinates", "coordinates_address", "coordinates_state"]
mysql_columns_exp = ["user_id bigint(20)", "message_id bigint(20) primary key", "message text", "created_time datetime", "in_reply_to_message_id bigint(20)", "in_reply_to_user_id bigint(20)", "retweet_message_id bigint(20)", "source varchar(128)", "lang varchar(4)", "time_zone varchar(64)", "friend_count int(6)", "followers_count int(6)", "coordinates varchar(128)", "coordinates_address varchar(64)", "coordinates_state varchar(3)", "index useriddex (user_id)"]


# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp, table='Fishbreakfast', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# twtSQL.userTimelineToMySQL(screen_name="Fishbreakfast", replace=True)
#
# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp, table='RandomTweets', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# twtSQL.randomSampleToMySQL(monthlyTables=True, replace = True)
#
#
# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp, table='selahwwbp', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# twtSQL.userTimelineToMySQL(screen_name="selahwwbp", replace=True)
#
#
#
# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp, table='CatTweets', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# twtSQL.tweetsToMySQL("search/tweets", q="cat", count="100", replace=True)
#
# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp, table='CatTweetsLk', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# twtSQL.tweetsToMySQL("statuses/lookup", q="cat", count="100", replace=True)
#
# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp, table='GeoLocTweets', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# twtSQL.tweetsToMySQL("statuses/lookup", q="cat", count="100", replace=True)


# twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp,
#                                    table='NYC', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
# for t in twtSQL.apiRequest("statuses/filter", locations='-74,40,-73,41'):
#     print t
#

twtSQL = TwitterMySQL(db="selah", host='wwbp', api=api, SQLfieldsExp = mysql_columns_exp,
                                   table='allGeotags', geoLocate = lm.reverseGeocodeLocal, dropIfExists = True)
twtSQL.tweetsToMySQL("statuses/filter", locations='-180,-90,180,90')
#Yeilds many tweets without coordinate :/  why???
#how do I affect which columns i print out???

