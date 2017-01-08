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

signal_tweets=[]
g=nx.Graph()
non_signal_tweets=[]
minhashes={}

tweets_raw = open("abc.txt", 'r')
tweets_data=tweets_raw.read()
#loads data into a dataframe
tweets = []
for line in open('abc.txt'):
            try:
                tweets.append(json.loads(line))
            except:
                 pass   

def is_signal_tweet(tweet):
    """identifies a tweet as signal or not using the following RegEx

    is (that | this | it) true
    wh[a]*t[?!][?1]*
    ( real? | really ? | unconfirmed )
    (rumor | debunk)
    (that | this | it) is not true

    @param: input tweet text
    @output: true if the tweet is a signal tweet, false otherwise
    """
    tweet_id=tweet['id']
            texts=tweet['text']
            true_val=bool(re.search('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',texts))
            if true_val==True:
                        signal_tweets.append(tweet)
            else:
                        non_signal_tweets.append(tweet)

            pass


def connected_components(g):
    """Finds the connected components of a graph g"""
    pass


def gen_undirected_graph(min_hashes, threshold=0.6):
    """Generate undirected graph of minhashes"""
    pass


def min_hash(tweet):
    """Generates a minhash for a tweet
    example repo https://github.com/ekzhu/datasketch
    """
    pass


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
    pass


def assign_cluster_to_non_signal_tweets():
    """capture all non-signal tweets that match any cluster
    """
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
