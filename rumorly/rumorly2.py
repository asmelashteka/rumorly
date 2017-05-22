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
from train_classifier import classify

reg_ex=re.compile(r"(\bis\s*(that\s*|this\s*|it\s*)true\s?[?]*)|\breal\b|reall[y?]*|unconfirmed|\brumor\b|debunk|(this\s*|that\s*|it\s*)is\s?not\s*true|\bwha[t?!]+\b",re.IGNORECASE)

thr=0.6
no_of_perm=100
signal_tweets=[]
non_signal_tweets=[]
signal_id_texts={}
non_signal_id_texts={}


TWEETS = Queue()
# special signal to mark next window
_sentinel = object()

def is_signal_tweet(tweet_text):
    if reg_ex.search(tweet_text):
        return True
    else:
        return False

def extract_summary(list_signal_tweets):
    """
    For each cluster extracts statement that summarizes the tweets in a signal cluster
    Args:
    param: Set of tweet ids

    Returns:
    Most frequent and continuous substrings (3grams that
    appear in more than 80% of the tweets) in order.
    """

    no_of_tweets=len(list_signal_tweets)
    req_cutoff=0.8*no_of_tweets
    words_list=set()
    shinglesincluster =[]
    for each_tweet in list_signal_tweets:
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


def gen_dstreams(window=600):
    '''generates discrete tweet streams.
    simulates this by adding a sentinel at every window
    #TODO: timed _sentinel insertion

    @param window in seconds
    '''
    start_time = time.time()
    stream = twitter.STREAMING_API(key=1, payload={})
    for tweet in stream.run():
        tweet_lang=tweet.get('lang')
        if tweet_lang in ('en','en-gb'):
            TWEETS.put(tweet)
        if int(time.time() - start_time) % window == 0:
            TWEETS.put(_sentinel)
            time.sleep(1)

def start_twitter_stream():
    '''launches Twitter stream'''
    t = threading.Thread(target=gen_dstreams)
    t.deamon = True
    t.start()


def pipeline():
    start_twitter_stream()
    while True:
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
            decision=classify(features)
            if 0 in decision:
                print("Probably Non-Rumor")
            else:
                print("Probably Rumor")
            
if __name__ == '__main__':
	pipeline()








