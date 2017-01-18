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
            texts=tweet['text']
            true_val=bool(re.search('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',texts))
            if true_val==True:
                        signal_tweets.append(tweet)
            else:
                        non_signal_tweets.append(tweet)

            pass


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


def gen_undirected_graph(min_hashes, threshold=0.6):
    """Generate undirected graph of minhashes"""
            k=list(minhashes.keys())
            l=list(minhashes.values())
            for i in range(0,len(k)-1):
                        for j in range((i+1),len(k)):
                                    a=l[i]
                                    b=l[j]
                                    c=jaccard_similarity(a,b)
                                    if (c>treshold):##change this 
                                                g.add_edge(k[i],k[j])
                                    else:
                                                g.add_node(k[i])
                                                g.add_node(k[j])
            nx.draw(g,with_labels=True)
            #plt.show()
            return g

def min_hash(tweet):
    """Generates a minhash for a tweet
   "" example repo https://github.com/ekzhu/datasketch""
  
            texts=tweet['text']
            docid=tweet['id']
            sentence=(texts.translate(non_bmp_map))
            words = sentence.split(" ")
            shinglesInDoc = set()
            for index in range(0, len(words) - 2):
                        shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
                        shinglesInDoc.add(shingle)
            m = MinHash(num_perm=50)
            for d in shinglesInDoc:
                        m.update(d.encode('utf8'))
            minhashes.update({docid:m})
            pass
def jaccard_similarity(a,b):
            return a.jaccard(b)
            
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
                        pres_cluster=cluster
                        no_of_tweets=len(pres_cluster)
                        req_cutoff=0.8*no_of_tweets
                        words_list=[]
                        cluster_df=signal_tweets['id'].isin(req_cluster)
                        tr_val=pd.Series(cluster_df)
                        present_df=signal_tweets[tr_val]
                        for index,row in present_df.iterrows():
                                    shinglesincluster ={}
                                    texts=row['text']
                                    docid=row['id']
                                    sentence=(texts.translate(non_bmp_map))
                                    words = sentence.split(" ")
                                    #print(words)
                                    for index in range(0, len(words) - 2):
                                                shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
                                                shinglesincluster.update({docid:shingle})
                                                #print(shinglesincluster)
                                                tot=Counter(shinglesincluster.values())
                                                ngrams=list(tot.keys())
                                                freq=list(tot.values())
                                                for i in range(len(freq)):
                                                            x=freq[i]
                                                            y=ngrams[i]
                                                            if x<req_cutoff:#change this
                                                                        words_list.append(y)
                                                            else:
                                                                        pass
                        sent=[]
                        sent= ' '.join(words_list)
                        words=sent.split()
                        wordlist=[]
                        sentence=[]
                        for word in words:
                                    if word not in wordlist:
                                                wordlist.append(word)
                                                sentence=' '.join(wordlist)
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
