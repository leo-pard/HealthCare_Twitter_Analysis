#!/usr/bin/enc python

"""
tweet_analyzer.py

Created by Anna A. Leonteva 16.10.13
"""
import os
import sys

from tweet_database import *
from tweet_cleanuper import *
from spam_filter import *

class TweetAnalyzer:

    def __init__( self ):
	"""
        Init a new TweetAnalyzer instance
	"""
	self.spam_analyzer = True
	self.sentiment_analyzer = True

    def run( self ):
        """
            Runs the tweet analyzer. It cleans up twitter messages, makes 
            spam detection & sentiment analisis
        """
        print "========================\nTweetAnalyzer starts\n========================"

	self.__loadTweetCleanupRules()        
        self.__loadTweetDatabase()
	self.__spamFilter()
	self.tweet_database.read( self.filter )
        print "========================\nTweetAnalyzer stoped\n========================"

    def __loadTweetCleanupRules( self ):
	""" 
	Create TweetCleanuper instanse
	"""
	try:
		self.tweet_cleanuper = TweetCleanuper()
	except:
		raise Exception( "Unexpected error in TweetAnalyzer: __loadTweetCleanupRules:",sys.exc_info()[0].__name__,os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename ),sys.exc_info()[2].tb_lineno,sys.exc_info()[1].message )


    def __loadTweetDatabase( self ):
	"""
	Create TweetDatabase instanse    
	"""
	try:
		self.tweet_database = TweetDatabase()
		self.tweet_database.load("dump", self.tweet_cleanuper)
	except:
		raise Exception( "Unexpected error in TweetAnalyzer: __loadTweetDatabase:",sys.exc_info()[0].__name__,\
			os.path.basename( sys.exc_info()[2].tb_frame.f_code.co_filename ),\
			sys.exc_info()[2].tb_lineno, \
			sys.exc_info()[1].message )
    
    def __spamFilter( self ):
	"""
	Create a spam filtering instance
	"""
	try:
		self.filter = SpamFilter( self.tweet_cleanuper)
	except:
		raise Exception( "Unexpected error in TweetAnalyzer: __spamFilter:",sys.exc_info()[0].__name__,\
			os.path.basename( sys.exc_info()[2].tb_frame.f_code.co_filename ),\
			sys.exc_info()[2].tb_lineno, \
			sys.exc_info()[1].message )
 
    
if __name__=='__main__':
	ta = TweetAnalyzer()
	ta.run()
