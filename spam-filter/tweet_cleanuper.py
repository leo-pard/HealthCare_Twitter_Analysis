#!/usr/bin/env python

"""
tweet_cleanuper.py

Created by Anna A. Leonteva 16.10.13
"""

import os
import sys
import unicodedata
import nltk
from nltk.corpus import stopwords
from collections import defaultdict


class TweetCleanuper:
    """
    Cleans up text of tweet - remove stopwords, puncuations and url links
    """

    def __init__ ( self ):
        """
        Creates new cleanup instance 
        """
        self.stopset = set( stopwords.words( 'english' ) )
        self.min_word_length = 2
        self.max_word_length = 12
        additional_stopwords = ["rt"]
        for stopword in additional_stopwords: self.stopset.add( stopword )

    def cleanup( self, text ): 
        """
        Create dict from the tweet text 
        """
        try:
		
		message = unicodedata.normalize('NFKD', text.lower()).encode('ascii','ignore') #"today gas"
		
		features = ""
		for word in message.split():
		    if self.test_word( word ):
			features = features + " "+ word

	        return features
        except:
	    print  "Unexpected error in TweetCleaunper: cleanup:",sys.exc_info()[0].__name__, os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename), sys.exc_info()[2].tb_lineno, sys.exc_info()[1].message
	    raise Exception
            return "err"

    def test_word(  self, word ):
        """
        Test word if it's belong to stopwords or begin from symbols "@" & "#"
        """

        if word in self.stopset \
                or len(word) < self.min_word_length \
                or len(word) > self.max_word_length \
                or word[0] == "@" \
                or word[0] == "#":
                return False
        else:
                return True

