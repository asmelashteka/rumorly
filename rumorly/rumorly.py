"""
Reproducing

Zhao, Zhe, Paul Resnick, and Qiaozhu Mei. "Enquiring minds: Early
detection of rumors in social media from enquiry posts." Proceedings of
the 24th International Conference on World Wide Web. ACM, 2015.

http://dl.acm.org/citation.cfm?id=2741637
"""

import re
import json
import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
import networkx as nx
import matplotlib.pyplot as plt
import sys
from collections import Counter

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
signal_tweets=[]
g=nx.Graph()
non_signal_tweets=[]
minhashes={}
lsh=MinHashLSH(threshold=0.6,num_perm=50)
minhashes={}

tweets_raw = open("abc.txt", 'r')
tweets_data=tweets_raw.read()
tweets = []
for line in open('abc.txt'):
            try:
                tweets.append(json.loads(line))
            except:
                 pass   

def is_signal_tweet(tweet_text):
    """identifies a tweet as signal or not using the following RegEx

    is (that | this | it) true
    wh[a]*t[?!][?1]*
    ( real? | really ? | unconfirmed )
    (rumor | debunk)
    (that | this | it) is not true

    @param: input tweet text
    @output: true if the tweet is a signal tweet, false otherwise
    """
    sentence=(tweet_text.translate(non_bmp_map))
    mat=re.search('(is\s?(that\s?|this\s[?]*|it\s?)true\s?[?]?)|(real|reall[y]*[?]*|unconfirmed)|(rumor|\\bdebunk\\b)|((this\s?|that\s?|it\s?)is\s?not\s?true)|wh[a]*[t]*[?!][?]*',sentence,re.IGNORECASE
                 )
    if mat:
        return True
    else:
        return False


def connected_components(g):
    """Finds the connected components of a graph g"""
    conn_comp=sorted(nx.connected_components(g),key=len,reverse=True)
    req_conn_comp=[]
    for each_cluster in conn_comp:
        if (len(each_cluster)>3):
            req_conn_comp.append(each_cluster)
        else:
            pass
                   
    return req_conn_comp


def gen_undirected_graph(min_hashes):
    for tweets,each_minhash in minhash.items():
        similar=lsh.query(each_minhash)
        for each_element in similar:
            g.add_edge(tweets,each_element)
    nx.draw(g,with_labels=True)
    plt.show()
    return g

def minhash(tweet_text):
    p=tweet_text.split()
    m=MinHash(num_perm=50)
    trigram=[]
    for i in range(len(p)-2):
        trigram.append(p[i]+p[i+1]+p[i+2])
        i=i+2
    for d in trigram:
        m.update(d.encode('UTF-8'))
    minhashes.update({tweet_text:m})
    lsh.insert("%s"%tweet_text,m)
    return m
            
def gen_signal_clusters(tweets):
    """clusters signal tweets based on overlapping content in tweets

    An undirected graph of tweets is built by including an edge joining
    any tweet pair with a jaccard similarity of 0.6. Minhash is used to
    efficiently compute the jaccard similarity. The connected components
    in this graph are the clusters.
    """
    min_hashes = []
    for tweet in tweets:
        h = min_hash(tweet)
        min_hashes.append(h)

    g = gen_undirected_graph(min_hashes, threshold=0.6)
    return connected_components(g)


def extract_summary(cluster):
    """extracts statement that summarizes the tweets in a signal cluster

    output the most frequent and continuous substrings (3-grams that
    appear in more than 80% of the tweets) in order.
    """
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
    tot=Counter(shinglesincluster)
    ngrams=list(tot.keys())
    freq=list(tot.values())
    for i in range(len(freq)):
        x=freq[i]
        y=ngrams[i]
        if x<req_cutoff:#change this
            words_list.append(y)
        else:
            pass
    sentence=[]
    sentence= ' '.join(words_list)
    return sentence


def assign_cluster_to_non_signal_tweets(sentence):
    """capture all non-signal tweets that match any cluster
    """
                        shingles_in_sent=set()
                        sent_tokens=sentence.split()
                        for index in range(0, len(sent_tokens) - 2):
                                    shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
                                    shingles_in_sent.add(shingle)
                        m=MinHash(num_perm=50)
                        for d in shinglesInDoc:
                                    m.update(d.encode('utf8'))
                        sent_minhash=m
                        a=list(non_signal_minhashes.keys())
                        b=list(non_signal_minhashes.values())
                        for s in range(len(b)):
                                    x=b[s]
                                    y=a[s]
                                    j=jaccard_similarity(x,sent_minhash)
                                    if j>treshold:
                                                cluster.add(y)
                                    else:
                                                pass


def rank_candidate_clusters():
    """rank candidate clusters in order of likelihood
    that their statements are rumors

    statistical features e.g.,
    percentage of signal tweets,
    avg tweet length,
    nof tweets,
    nof retweets
    """
    pass


def gen_stream():
    """Generates stream of tweets"""
    pass


def pipeline():
    """real-time rumor detection pipeline"""
    for tweet in gen_stream():
        if is_signal_tweet(tweet):
            clusters = gen_signal_tweets(tweet)
        else:
            compare_with_non_signal_tweets(tweet)

        rank_candidate_clusters()


if __name__ == '__main__':
    pipeline()
