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


from .twitter import STREAMING_API


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
lsh_signal=MinHashLSH(threshold=0.6,num_perm=50)
lsh_non_signal=MinHashLSH(threshold=0.6,num_perm=50)
g=nx.Graph()
all_tweets=[]
signal_tweets=[]
non_signal_tweets=[]
signal_id_text={}
non_signal_id_text={}
signal_minhashes={}
non_signal_minhashes={}


def is_signal_tweet(tweet_text):              
    """
    identifies a tweet as signal or not using the following RegEx
    is (that | this | it) true
    wh[a]*t[?!][?1]*
    ( real? | really ? | unconfirmed )
    (rumor | debunk)
    (that | this | it) is not true
    Args:
    @param(str): input tweet text
    @output: true if the tweet is a signal tweet, false otherwise
    """              
    sentence = (tweet_text.translate(non_bmp_map))
    matches = bool(re.search('(is\s?(that\s?|this\s?|it\s?)true\s?[?]?)|^real$|^reall[y]*[\s]?[?]*$|^unconfirmed$|rumor|debunk|(this\s?|that\s?|it\s?)is\s?not\s?true|wh[a]*[t]*[?!][?]*',sentence,re.IGNORECASE))
    return matches


def minhash(tweet_text,tweet_id,minhashes_dict,lsh_index):   
    """
    Generate a minhash from tweet_text and appends it to dictionary with text as key and appends to lsh index
    Args:
    param1(str): "text" part of the tweet
    param2(dictionary):Dictionary containing the {tweet_text:minhash(tweet_text)} items
    param3(lsh index):LSH Dictionary optimised for a particular treshold which accepts minhash objects
    
    Returns:
    Minhash value of the tweet-text and appends it to the lsh index and minhashes dictionary.
    """
    sentence=(tweet_text.translate(non_bmp_map))
    words = sentence.split(" ")
    m = MinHash(num_perm=50)
    for d in words:
        m.update(d.encode('UTF-8'))
    minhashes_dict.update({tweet_id:m})
    lsh_index.insert("%d"%tweet_id,m)
    return m

def generate_undirected_graph(tweet_id,min_hash):
    """
    An undirected graph of tweets is built by including an edge joining
    any tweet pair with a jaccard similarity of 0.6. Minhash is used to
    efficiently compute the jaccard similarity. The connected components
    in this graph are the clusters.
    
    Args:
    param(dictionary): Dictionary containing {text:minhash} items
        
    Returns:
    Graph, where nodes are tweet_texts and edges are formed between texts if they are similar by value greater than threshold
    
    """
    similar=lsh_signal.query(min_hash)
    g.add_node(tweet_id)
    for each in similar:
        g.add_edge(tweet_id,each)
    return g 

def connected_components(g):  
    """
    From the undirected graph generated by the function-gen_undirected_graph(), 
    the graph is filtered to include only the connected components that include more than the threshold number of nodes
    
    Args:
    param(graph): Graph containing clusters of connected components
    
    Returns:
    Clusters containing more than threshold no of tweets
    
    """
    cconn_comp=sorted(nx.connected_components(g),key=len,reverse=True)
    req_conn_comp=[]
    for each_cluster in conn_comp:
        if (len(each_cluster)>3):
            req_conn_comp.append(each_cluster)
        else:
            pass
    return req_conn_comp

def extract_summary(cluster):  
    """
    For each cluster extracts statement that summarizes the tweets in a signal cluster
    Args:
    param: Set of tweet ids
    
    Returns:
    Most frequent and continuous substrings (3-grams that
    appear in more than 80% of the tweets) in order.
    """
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
    """
    From a sentence that summarizes each cluster,the sentence is matched against 
    nog-signal tweet_texts to match the tweets that belong to the cluster but donot contain signal patterns
    Args:
    param(str):Statement that summarizes each cluster
    
    Returns:
    Tweet_texts that belong to the cluster
    
    """
    shingles_in_sent=set()
    string=(sentence.translate(non_bmp_map))
    sent_tokens=string.split()
    m=MinHash(num_perm=50)
    for d in sent_tokens:
        m.update(d.encode('UTF-8'))
    similar_nonsignal_tweets=lsh_non_signal.query(m)
    return similar_nonsignal_tweets


def gen_stream(fin=None):
    """Generates stream of tweets.
    using the Twitter public sample stream.
    """
    stream  = twitter.STREAMING_API(key=1, payload={})
    for tweet in stream.run():
        yield tweet


def pipeline():
    """real-time rumor detection pipeline"""
    for tweet in gen_stream():
        tweet_id=tweet['id']
        tweet_text=tweet['text'].translate(non_bmp_map)
        if is_signal_tweet(tweet_text):
            signal_tweets.append(tweet)
            signal_id_text.update({tweet_id:tweet_text})
            minhash(tweet_text,tweet_id,signal_minhashes,lsh_signal)
        else:
            non_signal_tweets.append(tweet)
            non_signal_id_text.update({tweet_id:tweet_text})
            minhash(tweet_text,tweet_id,non_signal_minhashes,lsh_non_signal)
    for key,value in signal_minhashes.items():
        graph=generate_undirected_graph(key,value)
    conn_comp=connected_components(graph)
    for each_cluster in conn_comp:
        sig_tweets=[]
        for each_id in each_cluster:
            for k,v in signal_id_text.items():
                if each_id==k:
                    sig_tweets.append(v)

        non_sig_tweets=[]
        sent=extract_summary(sig_tweets)
        sim_non_sig_tweets=non_signal_tweets_to_cluster(sent)
        for each in sim_non_signal_tweets:
            for k,v in non_signal_id_text:
                if each==k:
                    non_sig_tweets.append(v)

        tot_tweets=sig_tweets+non_sig_tweets
        features=gen_statistical_features(tot_tweets,sig_tweets)
        #each|=set(sim_non_signal_tweets)


if __name__ == '__main__':
    pipeline()
