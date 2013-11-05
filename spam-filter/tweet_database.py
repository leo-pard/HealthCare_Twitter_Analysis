#!/usr/bin/env python

"""
tweet_database.python

Created by Anna A. Leonteva 16.10.13
"""

import os
import sys
import json
import ast
import redis
import string

from tweet_cleanuper import *
from spam_filter import *

class TweetDatabase:
        """
        Get twitter data from json files, does some simple cleanup, save then
        into redis-databese.
        """

        def __init__( self ):
            """
                New TweetDatabase instance
            """
	    #Init Redis Database
            self.database = redis.Redis(host='localhost', port=6379, db=0)
	    #Init fields for database
            self.fields = ['name','created_at','id','screen_name','followers_count','friends_count','time_zone','text']
            #Counter of tweets
	    #self.tweets_count = 0

        def load( self, path, cleanuper ):
            """
                Get tweets from json files and load them to redis
            """
	    try:
		self.database.flushall()
    		files = self.__get_file_list( path )
    		for filename in files:
            	    with open( os.path.join( path, filename )) as filehandle:
            		content = json.loads(filehandle.read())
			for tweet in content:
			    if ( tweet['lang'] != 'en' ): continue;
			    tweet_info = []
			    for fetched_data in self.fields:
                                if ( fetched_data  in tweet ):    
				    if ( fetched_data == 'text' ):
					result = cleanuper.cleanup(tweet[fetched_data])
				    else: result = tweet[fetched_data]
				    tweet_info.append( result )
				else: 
                                    tweet_info.append( tweet['user'][fetched_data] )

			    #Put the tweet info in Redis database with key "string id" 
			    
			    for t in tweet_info:
				self.database.rpush(tweet['id_str'], t)
				#self.database.set(tweet['id_str'], tweet_info ) 

            except:
		print  "Unexpected error in TweetDatabase: load:",sys.exc_info()[0].__name__, \
				    os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),\
				    sys.exc_info()[2].tb_lineno,sys.exc_info()[1].message
		raise Exception

	def read( self, filter ):
	    """
	    Read info from database by key
	    """
	    try:
		t_info = []
		keys = self.database.keys('*')
		for key in keys:
		    print key
		    #t_info =  self.database.get(key) 
		    t_info = self.database.lindex (key, 7 )
		    filter.classify( t_info )
		    #print t_info

	    except:
		print  "Unexpected error in TweetDatabase: read:",sys.exc_info()[0].__name__, \
				    os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename),\
				    sys.exc_info()[2].tb_lineno,sys.exc_info()[1].message
		raise Exception

        def __get_file_list( self, path ):
            """
                Make list of files in dir, which is located in path
            """
            files = os.listdir( path )
            return files
