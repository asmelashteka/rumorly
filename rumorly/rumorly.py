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
from scipy import stats as scistat 
import networkx as nx
import matplotlib.pyplot as plt
import sys
from collections import Counter

non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
lsh_signal=MinHashLSH(threshold=0.6,num_perm=50)
lsh_non_signal=MinHashLSH(threshold=0.6,num_perm=50)
g=nx.Graph()
tweets = []
signal_tweets=[]
non_signal_tweets=[]
signal_minhashes={}
non_signal_minhashes={}




def is_signal_tweet(tweet_text):               ####check for signal and append the tweets to list of signal or non_signal_tweets
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
    
    
def minhash(tweet_text,signal_minhashes,lsh_signal):   ###generate minhash and insert into respective index and minhash dictionaries
    sentence=(tweet_text.translate(non_bmp_map))
    words = sentence.split(" ")
    shinglesInDoc = set()
    for index in range(0, len(words) - 2):
        shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
        shinglesInDoc.add(shingle)
    m = MinHash(num_perm=50)
    for d in shinglesInDoc:
        m.update(d.encode('UTF-8'))
    signal_minhashes.update({tweet_id:m})
    lsh_signal.insert("%d"%tweet_id,m)
    return m

def gen_undirected_graph(min_hashes):    ###from list of minhashes(signal or non_signal), for each minhash, query the lsh index and form a graph with ouput values
    for tweet,each_minhash in minhash.items():
        similar=lsh.query(each_minhash)
        for each_element in similar:
            g.add_edge(tweet,each_element)
    nx.draw(g,with_labels=True)
    plt.show()
    return g

def connected_components(g):  ####from the graph, extract the set of tweets which have more than 3 tweets in each set
    """Finds the connected components of a graph g"""
    conn_comp=sorted(nx.connected_components(g),key=len,reverse=True)
    req_conn_comp=[]
    for each_cluster in conn_comp:
        if (len(each_cluster)>3):
            req_conn_comp.append(each_cluster)
        else:
            pass               
    return req_conn_comp

            
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


def extract_summary(cluster):  ##cluster is the each set of tweets in the req_conn_comp
    """extracts statement that summarizes the tweets in a signal cluster

    output the most frequent and continuous substrings (3-grams that
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


def assign_cluster_to_non_signal_tweets(sentence):  ####form minhash of sentence,create minhashes of non_signal_tweets,query sentence_minhash with non_signal minahshes lsh 
    """capture all non-signal tweets that match any cluster
    """
    shingles_in_sent=set()
    string=(tweet_text.translate(non_bmp_map))
    sent_tokens=string.split()
    for index in range(0, len(sent_tokens) - 2):
        shingle = words[index] + " " + words[index + 1] + " " + words[index + 2]
        shingles_in_sent.add(shingle)
    m=MinHash(num_perm=50)
    for d in shinglesInDoc:
        m.update(d.encode('UTF-8'))
    similar_nonsignal_tweets=lsh_non_signal.query(m)
    return similar_nonsignal_tweets    
                        
                                 


def rank_candidate_clusters():
    """rank candidate clusters in order of likelihood  ###these tweets are used for generating training sets
    that their statements are rumors

    statistical features e.g.,
    percentage of signal tweets,
    avg tweet length,
    nof tweets,
    nof retweets
    """
"""   
false_tweets_ids=[]
true_tweets_ids=[]
false_tweets=[]
true_tweets=[]
false_signal_tweets=[]
true_signal_tweets=[]
for keys,values in train_set.items():
            if values=='false':
                        false_tweets_ids.append(keys)
            elif values=='true':
                       true_tweets_ids.append(keys)
            else:
                        pass
false_tweets_ids=[int(i) for i in false_tweets_ids]

true_tweets_ids=[int(i) for i in true_tweets_ids]



for each_id in false_tweets_ids:
    for each_tweet in tweets:
        if each_id==each_tweet['id']:
            false_tweets.append(each_tweet)
for each_id in true_tweets_ids:
    for each_tweet in tweets:
        if each_id==each_tweet['id']:
            true_tweets.append(each_tweet)


for each in false_tweets:
    texts=each['text']
    sentence=(texts.translate(non_bmp_map))
    mat=re.match('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',sentence)
    if mat:
        false_signal_tweets.append(each)
    else:
        pass


for each in true_tweets:
    texts=each['text']
    sentence=(texts.translate(non_bmp_map))
    mat=re.match('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',sentence)
    if mat:
        true_signal_tweets.append(each)
    else:
        pass
 
 """



def feat1(all_tweets,signal_tweets):
    a=len(signal_tweets)
    b=len(all_tweets)
    c=a/b
    return c


def feat2(all_tweets,signal_tweets):
    all_sent=[]
    sig_sent=[]
    for each_tweet in all_tweets:
        texts=each['text']
        sentence=(texts.translate(non_bmp_map))
        words=sentence.split(" ")
        all_sent.append(words)
    all_sent=reduce(lambda x,y: x+y,all_sent)
    all_count=Counter(all_sent)
    all_freq=list(all_count.values())
    tot_sum=sum(all_freq)
    for i in range(len(all_freq)):
        all_freq[i]=all_freq[i]/tot_sum
    all_entr=scistat.entropy(all_freq)

    for each_tweet in signal_tweets:
        texts=each['text']
        sentence=(texts.translate(non_bmp_map))
        words=sentence.split(" ")
        sig_sent.append(words)
    sig_sent=reduce(lambda x,y: x+y,sig_sent)
    sig_count=Counter(sig_sent)
    sig_freq=list(sig_count.values())
    tot_sig_sum=sum(sig_freq)
    for i in range(len(sig_freq)):
        sig_freq[i]=sig_freq[i]/tot_sig_sum
    sig_entr=scistat.entropy(sig_freq)
    
    entr=sig_entr/all_entr
    return entr


def feat3(signal_tweets):
    l=[]
    for each in signal_tweets:
        texts=each['text']
        sentence=(texts.translate(non_bmp_map))
        words=sentence.split(" ")
        l.append(len(words))
    return np.mean(l)


def feat4(all_tweets):
    a=feat3(all_tweets)
    return a


def feat5(signal_tweets,all_tweets):
    a=feat3(signal_tweets)
    b=feat3(all_tweets)
    return (a/b)


def feat6(signal_tweets):
    signal_retweets=0
    for each in signal_tweets:
        for each_key in each.keys():
            if each_key=='retweeted_status':
                signal_tweets=signal_retweets+1
    
    b=(signal_retweets/len(signal_tweets))
    return b

def feat7(all_tweets):
    d=feat6(all_tweets)
    return d


def feat8(signal_tweets):
    url_count=[]
    for each in signal_tweets:
        texts=each['text']
        sentence=(texts.translate(non_bmp_map))
        words=sentence.split(" ")
        i=words.count("http:")
        j=words.count("https:")
        k=a+b
        url_count.apend(k)
    return np.mean(url_count)

def feat9(all_tweets):
    c=feat8(all_tweets)
    return c

def feat10(signal_tweets):
    c=[]
    for each in signal_tweets:
        texts=each['text']
        sentence=(texts.translate(non_bmp_map))
        s=re.findall('(?<=^|(?<=[^a-zA-Z0-9-\.]))#([A-Za-z]+[A-Za-z0-9_]+)',sentence)
        no_of_hash=len(s)
        c.append(no_of_hash)
    return np.mean(c)

def feat11(all_tweets):
    a=feat10(all_tweets)
    return a

def feat12(signal_tweets):
    c=[]
    for each in signal_tweets:
        texts=each['text']
        sentence=(texts.translate(non_bmp_map))
        s=re.findall('(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z]+[A-Za-z0-9_]+)',sentence)
        no_of_hash=len(s)
        c.append(no_of_hash)
    return np.mean(c)

def feat13(all_tweets):
    a=feat12(all_tweets)
    return a

def statistical_features(all_tweets,signal_tweets):
    f1=feat1(all_tweets,signal_tweets)
    f2=feat2()
    f3=feat3(signal_tweets)
    f4=feat4(all_tweets)
    f5=feat5(signal_tweets,all_tweets)
    f6=feat6(signal_tweets)
    f7=feat7(all_tweets)
    f8=feat8(signal_tweets)
    f9=feat9(all_tweets)
    f10=feat10(signal_tweets)
    f11=feat11(all_tweets)
    f12=feat12(signal_tweets)
    f13=feat13(all_tweets)
    return [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]


def gen_stream():
    """Generates stream of tweets"""

 

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
