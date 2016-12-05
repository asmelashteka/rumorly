"""
Reproducing

Zhao, Zhe, Paul Resnick, and Qiaozhu Mei. "Enquiring minds: Early
detection of rumors in social media from enquiry posts." Proceedings of
the 24th International Conference on World Wide Web. ACM, 2015.

http://dl.acm.org/citation.cfm?id=2741637
"""

import json
import pandas as pd
from datetime import datetime
import time
import re

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
    df=pd.DataFrame(tweets)
#extract tweets which are replies of other tweets
df1=df[df['in_reply_to_status_id'].notnull()]
df2=pd.DataFrame()
#check for pattern matching 
df2=df1.text.str.contains('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',regex=True)
is_true=pd.Series(df2)
print(is_true)
df3=df1[is_true]
rt_data=pd.DataFrame()
rt_data=df.merge(df3[['in_reply_to_status_id']].drop_duplicates(), left_on='id', right_on='in_reply_to_status_id', how='right')
return rt_data
    pass


def gen_signal_clusters(stream, duration):
    """clusters signal tweets based on overlapping content in tweets

    An undirected graph of tweets is built by including an edge joining
    any tweet pair with a jaccard similarity of 0.6. Minhash is used to
    efficiently compute the jaccard similarity. The connected components
    in this graph are the clusters.
    """
    pass


def extract_summary(cluster):
    """extracts statement that summarizes the tweets in a signal cluster

    output the most frequent and continuous substrings (3-grams that
    appear in more than 80% of the tweets) in order.
    """
    pass


def capture_non_signal_tweets():
    """capture all non-signal tweets that match any cluster
    """
    pass


def rank_candidate_clusters():
    """rank candidate clusters in order of likelihood
    that their statements are rumors
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
