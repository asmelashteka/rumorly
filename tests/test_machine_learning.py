import re
import json
import numpy as np
import pandas as pd
from datasketch import MinHash, MinHashLSH
from collections import Counter
from functools import reduce
from scipy import stats as scistat
from sklearn import svm
import networkx as nx
import matplotlib.pyplot as plt
import sys


non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
tweets_raw = open("abc.txt", 'r')
tweets_data=tweets_raw.read()
lsh_signal=MinHashLSH(threshold=0.6,num_perm=50)
lsh_non_signal=MinHashLSH(threshold=0.6,num_perm=50)
#loads data into a dataframe
tweets = []
for line in open('abc.txt'):
            try:
                tweets.append(json.loads(line))
            except:
                 pass
signal_tweets=[]
non_signal_tweets=[]

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
        k=i+j
        url_count.append(k)
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
    f2=feat2(all_tweets,signal_tweets)
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


for each in tweets:
    texts=each['text']
    sentence=(texts.translate(non_bmp_map))
    mat=re.match('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',sentence)
    if mat:
        signal_tweets.append(each)
    else:
        pass

for each in tweets:
    texts=each['text']
    sentence=(texts.translate(non_bmp_map))
    mat=re.match('(is(that|this|it)true?)|(real|really?|unconfirmed)|(rumor|debunk)|((this|that|it)is not true)|wh[a]*t[?!][?]*',sentence)
    if mat:
        pass
    else:
        non_signal_tweets.append(each)

c=statistical_features(tweets,signal_tweets)
d=statistical_features(tweets,non_signal_tweets)


X=np.array([c,d])
y=[0,1]

clf=svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)


        
"""output:

print(clf.predict([[0.4629629629629629, 1.0, 14.23076923076923, 4.074074074074074, 0.0111336032388663, 0.0, 0.0, 0.0, 0.0, 0.93076923076923073, 0.10370370370370372, 0.88461538461538458, 0.65185185185185186]]))
[1]
print(clf.predict([[0.037037037037037035, 1.0, 10.0, 14.074074074074074, 0.71052631578947367, 0.0, 0.0, 0.0, 0.0, 0.0, 0.70370370370370372, 0.0, 0.85185185185185186]]))
[0]       

"""


