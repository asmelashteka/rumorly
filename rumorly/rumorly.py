import sys
import time
import re
import json
import gzip
import random
import threading
from random import randint
from queue import Queue
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np

import twitter
from twitter import STREAMING_API
from create_lsh import create_lsh,create_clusters,near_duplicates
from gen_features import gen_statistical_features
from train_classifier import svm_classify,decision_classify

reg_ex=re.compile(r"(is\s*(that\s*|this\s*|it\s*)true\s?[?]*)|\breal\s*[?]|\breally\s*[?]+|\bunconfirmed|\brumor|\bdebunk|(this\s*|that\s*|it\s*)is\s?not\s*true|wha*t[?!][?1]*|\bfake\s*news",re.IGNORECASE)

TWEETS = Queue()
# special signal to mark next window
_sentinel = object()

def is_signal_tweet(tweet_text):
	"""
	Search for presence of signal pattern in the tweet_text
	Args:
	Param: tweet_text
	Returns:
	True if signal pattern is found, False otherwise
	
	"""

	if reg_ex.search(tweet_text):
		return True
	else:
		return False

def extract_summary(list_signal_tweet_texts):
	"""
	For each cluster extracts statement that summarizes the tweets in a signal cluster
	Args:
	param: Set of tweet texts
	Returns:
	Most frequent and continuous substrings (3grams that
	appear in more than 80% of the tweets) in order.
	"""

	no_of_tweets=len(list_signal_tweet_texts)
	req_cutoff=0.8*no_of_tweets
	words_list=set()
	shinglesincluster =[]
	for each_tweet in list_signal_tweet_texts:
		words = each_tweet.split(" ")
		for index in range(0, len(words) - 2):
			shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
			shinglesincluster.append(shingle)
	tot=dict(Counter(shinglesincluster))
	for k,v in tot.items():
		if v>=req_cutoff:
			words_list.add(k)
	sentence= ' '.join(words_list)
	return sentence

def gen_stream():
	with open("filename") as f:
		for each in f:
			yield json.loads(each)

def gen_dstreams(time_window):
	'''generates discrete tweet streams.
	simulates this by adding a sentinel at every window
	#TODO: timed _sentinel insertion
	@param window in seconds
	'''
	start_time = datetime.datetime.strptime('starttime of the tweet(ex time.now()', '%a %b %d %H:%M:%S +0000 %Y')
	count=0
	for tweet in gen_stream():
		TWEETS.put(tweet)
		times=tweet.get("created_at")
		tweet_time=datetime.datetime.strptime(times, '%a %b %d %H:%M:%S +0000 %Y')
		if ((tweet_time-start_time).total_seconds())>time_window:
			TWEETS.put(_sentinel)
			start_time=datetime.datetime.strptime(times, '%a %b %d %H:%M:%S +0000 %Y')



def pipeline():
	gen_dstreams()
	while True:
		signal_tweets=[]
		non_signal_tweets=[]
		signal_id_texts={}
		non_signal_id_texts={}
		svm_rank={}
		dec_rank={}
		while True:
			tweet = TWEETS.get()
			if tweet is _sentinel:
				break
			tweet_id=tweet.get('id')
			tweet_text=tweet.get('text')
			if(is_signal_tweet(tweet_text)):
				signal_id_texts.update({tweet_id:tweet_text})
				signal_tweets.append(tweet)
			else:
				non_signal_id_texts.update({tweet_id:tweet_text})
				non_signal_tweets.append(tweet)
		lsh_dict_sig,doc_to_lsh_sig,hashcorp_sig=create_lsh(signal_id_texts,no_of_perm,thr)
		clusters=create_clusters(lsh_dict_sig,doc_to_lsh_sig,hashcorp_sig,thr)
		for keys,values in clusters.items():
			sig_tweet_texts=[]
			sig_tweets_cluster=[]
			for each in values:
				sig_tweet_texts.append(signal_id_texts[each])
			for tweet in signal_tweets:
				if tweet['id']==each:
					sig_tweets_cluster.append(tweet)
			sent=extract_summary(sig_tweet_texts)
			print("Rumor statement is: ")
			print(sent)
			non_sig_tweets_cluster=[]
			non_signal_id_texts.update({'11111111':sent})
			lsh_dict_nonsig,doc_to_lsh_nonsig,hashcorp_nonsig=create_lsh(non_signal_id_texts,no_of_perm,thr)
			non_sig_tweets=near_duplicates('11111111',lsh_dict_nonsig,doc_to_lsh_nonsig,thr)
			for each_id in non_sig_tweets:
				for tweet in non_signal_tweets:
					if tweet['id']==each_id:
						non_sig_tweets_cluster.append(tweet)
			all_tweets=sig_tweets_cluster+non_sig_tweets_cluster
			features=gen_statistical_features(all_tweets,sig_tweets_cluster)
			svm_decision=svm_classify(features)
			svm_rank.update({sent:svm_decision[0][0]})
			tree_decision=decision_classify(features)
			dec_rank.update({sent:tree_decision[0][0]})
		ranked_svm=(sorted(svm_rank,key=svm_rank.get,reverse=True))
		ranked_dec=(sorted(dec_rank,key=dec_rank.get,reverse=True))
		a=1
		b=1
		print("Ranking Using SVM")
		for each in ranked_svm:
			print("rank {}".format(a),each)
			a=a+1
			print("\n")
		print("ranking Using Decision Tree")
		for each in reanked_dec:
			print("rank {}".format(b),each)
			b=b+1
			print("\n")


if __name__ == '__main__':
	pipeline()
