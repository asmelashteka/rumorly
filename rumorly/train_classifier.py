import re
import json
import numpy as np
import sys
from datasketch import MinHash, MinHashLSH
from collections import Counter
from functools import reduce
from scipy import stats as scistat
from sklearn import svm
from gen_features import gen_statistical_features
sig_tweets_rumor=[]
all_tweets_rumor=[]
sig_tweets_non_rumor=[]
all_tweets_non_rumor=[]

reg_ex=re.compile(r"(\bis\s*(that\s*|this\s*|it\s*)true\s?[?]*)|\breal\b|reall[y?]*|unconfirmed|\brumor\b|debunk|(this\s*|that\s*|it\s*)is\s?not\s*true|\bwha[t?!]+\b",re.IGNORECASE)

def is_signal_tweet(tweet_text):
    if reg_ex.search(tweet_text):
        return True
    else:
        return False

with open("all_rumors.txt") as f:
    for each in json.load(f):
        if is_signal_tweet(each['text']):
            sig_tweets_rumor.append(each)
        all_tweets_rumor.append(each)

rumor_features=gen_statistical_features(all_tweets_rumor,sig_tweets_rumor)


with open("all_non_rumors.txt") as f:
    for each in json.load(f):
        if is_signal_tweet(each['text']):
            sig_tweets_non_rumor.append(each)
        all_tweets_non_rumor.append(each)


non_rumor_features=gen_statistical_features(all_tweets_non_rumor,sig_tweets_non_rumor)


X=np.array([rumor_features,non_rumor_features])
y=[1,0]

clf=svm.SVC(kernel='linear', C=1.0)
clf.fit(X,y)



def classify(feature_list):
    return clf.predict([feature_list])




