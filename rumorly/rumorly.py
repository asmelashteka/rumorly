"""
Reproducing
Zhao, Zhe, Paul Resnick, and Qiaozhu Mei. "Enquiring minds: Early
detection of rumors in social media from enquiry posts." Proceedings of
the 24th International Conference on World Wide Web. ACM, 2015.
http://dl.acm.org/citation.cfm?id=2741637
"""

import sys
import re
import json
import gzip
from collections import Counter
import random
from random import randint
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
import networkx as nx
import twitter
from twitter import STREAMING_API
import training
from training import train_classifier


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
lsh_signal=MinHashLSH(threshold=0.6, num_perm=50)
lsh_non_signal=MinHashLSH(threshold=0.6, num_perm=50)
g=nx.Graph()
all_tweets=[]
signal_tweets=[]
non_signal_tweets=[]
signal_id_text={}
non_signal_id_text={}
signal_minhashes={}
non_signal_minhashes={}


def is_signal_tweet(tweet_text):              
    matches = bool(re.search('(is\s?(that\s?|this\s?|it\s?)true\s?[?]?)|^real$|^reall[y]*[\s]?[?]*$|^unconfirmed$|rumor|debunk|(this\s?|that\s?|it\s?)is\s?not\s?true|wh[a]*[t]*[?!][?]*',tweet_text,re.IGNORECASE))
    return matches

def minhash(tweet_text,tweet_id,lsh_index,minhashes_dict):   
    words = tweet_text.split(" ")
    trigrams=[]
    for i in range(len(words)-2):
        trigrams.append(words[i]+words[i+1]+words[i+2])
    m = MinHash(num_perm=50)
    for d in trigrams:
        m.update(d.encode('UTF-8'))
    minhashes_dict.update({tweet_id:m})
    lsh_index.insert("tweet_id",m)
    return m
    
def generate_undirected_graph(tweet_id,min_hash):
    g.add_node(tweet_id)
    similar=lsh_signal.query(min_hash)
    for each in similar:
        g.add_edge(tweet_id,each)

    

def connected_components(g):  
    conn_comp=sorted(nx.connected_components(g),key=len,reverse=True)
    req_conn_comp=[]
    for each_cluster in conn_comp:
        if (len(each_cluster)>3):
            req_conn_comp.append(each_cluster)
        else:
            pass
    return req_conn_comp

def extract_summary(cluster):  
    no_of_tweets=len(cluster)
    req_cutoff=0.8*no_of_tweets
    words_list=[]
    shinglesincluster =[]
    for each_tweet in cluster:
        sente=(each_tweet.translate(non_bmp_map))
        words = sente.split(" ")
        for index in range(0, len(words) - 2):
            shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
            shinglesincluster.append(shingle)
    tot=dict(Counter(shinglesincluster))
    for k,v in tot.items():
        if v>=req_cutoff:
            words_list.append(k)
    sentence= ' '.join(words_list)
    return sentence
    
def assign_cluster_to_non_signal_tweets(sentence): 
    shingles_in_sent=set()
    string=(sentence.translate(non_bmp_map))
    sent_tokens=string.split()
    m=MinHash(num_perm=50)
    for d in sent_tokens:
        m.update(d.encode('UTF-8'))
    similar_nonsignal_tweets=lsh_non_signal.query(m)
    return similar_nonsignal_tweets

def gen_stream(fin=None):
    stream  = twitter.STREAMING_API(key=1, payload={})
    for tweet in stream.run():
        try:
            yield (tweet['text'].translate(non_bmp_map),tweet['id'])
        except KeyError:
            pass


def pipeline():
    for each_tweet in gen_stream():
        tweet_id=str(each_tweet[1])
        tweet_text=each_tweet[0]
        try:
            if is_signal_tweet(tweet_text):
                signal_id_text.update({tweet_id:tweet_text})
                m=minhash(tweet_text,tweet_id,lsh_signal,signal_minhashes)
                gen_undirected_graph(tweet_id,m)
            else:
                minhash(tweet_text,tweet_id,lsh_non_signal,non_signal_minhashes)
                non_signal_id_text.update({tweet_id:tweet_text})                
        except ValueError:
            pass
        rumor_ids=connected_components(g)
        for each_cluster in rumor_ids:
        sig_tweets=[]
        non_sig_tweets=[]
        for each_id in each_cluster:
            for k,v in signal_id_text.items():
                if each_id==k:
                    sig_tweets.append(v)
        sent=extract_summary(sig_tweets)
        sim_non_sig_tweets=non_signal_tweets_to_cluster(sent)
        for each in sim_non_signal_tweets:
            for k,v in non_signal_id_text:
                if each==k:
                    non_sig_tweets.append(v)
        tot_tweets=sig_tweets+non_sig_tweets
        
    
        

            

if __name__ == '__main__':
    pipeline()
