#!/usr/bin/env python

"""
spam_filter.py

Created by Anna A. Leonteva 16.10.13
"""

import os
import sys
from nltk import NaiveBayesClassifier
from collections import defaultdict
import nltk.classify
from tweet_cleanuper import *

class SpamFilter:
    """
    SpamFilter trains a NaiveBayes classifier for detect wheater a tweet is 
    spam or ham. 
    """

    def __init__ ( self, cleanuper ):
        """
        Creates new SpamFilter instance.
        """
	self.cleanuper = cleanuper
        self.__init_naive_bayes( )

    def __make_featured_set( self, filelist, label ):
	"""
	    Create list of featured, which is labeled as 'spam' or 'ham'
	"""
	
        try:
            set = []
	    for f in filelist:
		text = open(f).read().lower().split()
	        features = dict( [ ( w, True )
				for w in text
				if self.cleanuper.test_word( w ) ] )
	        set.append(( features, label ))
		
	    return set
	except:
		    raise Exception( "Unexpected error in SpamFilter: __spamFilter:",sys.exc_info()[0].__name__,\
			os.path.basename( sys.exc_info()[2].tb_frame.f_code.co_filename ),\
			sys.exc_info()[2].tb_lineno, \
			sys.exc_info()[1].message )


    def __init_naive_bayes( self ):
        """
    	    Create and trains the NaiveBayes Classifier
        """
	try:
#		corpus_no = abs(int(raw_input('Enter the number (1-3) of corpus: ')))
#		while corpus_no == 0 or corpus_no > 3:
#		    corpus_no = abs(int(raw_input('Please the number of corpus from 1 to 2:' )))
		corpus = 'corpus2'#+str(corpus_no)
		
		path = os.path.join('corpora/',corpus)
		spam_path = os.path.join(path,'spam')
		ham_path = os.path.join(path,'ham')
		
		
		spam_dir = os.listdir(spam_path)
		ham_dir = os.listdir(ham_path)
		
		train_spam_filelist = [os.path.join(spam_path, f) for f in spam_dir]
		train_ham_filelist = [os.path.join(ham_path, f) for f in ham_dir]

		spam_size = len(train_spam_filelist)
		ham_size = len(train_ham_filelist)
		
		train_spam_set = self.__make_featured_set(train_spam_filelist,'spam')
		train_ham_set = self.__make_featured_set(train_ham_filelist,'ham')
		train_set = train_spam_set + train_ham_set
		
		self.classifier = NaiveBayesClassifier.train( train_set )

	except:
		    raise Exception( "Unexpected error in SpamFilter: __spamFilter:",sys.exc_info()[0].__name__,\
			os.path.basename( sys.exc_info()[2].tb_frame.f_code.co_filename ),\
			sys.exc_info()[2].tb_lineno, \
			sys.exc_info()[1].message )

    def classify( self, message ):
        """ 
        Classify features from db
        """
        try:
		features = defaultdict( list )
		
		for k in message.split():
		    features[k] = True
		
		print features
		print self.classifier.classify(features)

	except:
		    raise Exception( "Unexpected error in SpamFilter: classify:",sys.exc_info()[0].__name__,\
			os.path.basename( sys.exc_info()[2].tb_frame.f_code.co_filename ),\
			sys.exc_info()[2].tb_lineno, \
			sys.exc_info()[1].message )



