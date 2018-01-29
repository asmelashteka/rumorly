import re
import json
import numpy as np
from collections import Counter
from functools import reduce
from scipy import stats as scistat
from sklearn import svm
import sys


def gen_statistical_features(all_tweets,signal_tweets):
    """
    Generates Statistical features from tweets
    
    Input: Labelled Tweets
    
    Output: Feature Vector
    """
    
    def ratio_signal_all(all_tweets,signal_tweets):
        a=len(signal_tweets)
        b=len(all_tweets)
        c=a/b
        return c


    def ratio_entr_word_freq(all_tweets,signal_tweets):
        all_sent=[]
        sig_sent=[]
        for each_tweet in all_tweets:
            texts=each_tweet['text']
            words=texts.split(" ")
            all_sent.append(words)
        all_sent=reduce(lambda x,y:x+y,all_sent)
        all_count=Counter(all_sent)
        all_freq=list(all_count.values())
        tot_sum=sum(all_freq)
        for i in range(len(all_freq)):
            all_freq[i]=all_freq[i]/tot_sum
        all_entr=scistat.entropy(all_freq)
        for each_tweet in signal_tweets:
            texts=each_tweet['text']
            words=texts.split(" ")
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


    def avg_no_words_signal(signal_tweets):
        l=[]
        for each in signal_tweets:
            texts=each['text']
            words=texts.split(" ")
            l.append(len(words))
        return np.mean(l)


    def avg_no_words_alltweets(all_tweets):
        a=avg_no_words_signal(all_tweets)
        return a


    def rat_avg_words(signal_tweets,all_tweets):
        a=avg_no_words_signal(signal_tweets)
        b=avg_no_words_alltweets(all_tweets)
        return (a/b)


    def perc_retweet_signal(signal_tweets):
        signal_retweets=0
        for each in signal_tweets:
            for each_key in each.keys():
                if each_key=='retweeted_status':
                    signal_retweets=signal_retweets+1

        b=(signal_retweets/len(signal_tweets))
        return b

    def perc_retweet_alltweets(all_tweets):
        d=perc_retweet_signal(all_tweets)
        return d


    def avg_urls_signal(signal_tweets):
        url_count=[]
        for each in signal_tweets:
            texts=each['text']
            words=texts.split(" ")
            i=words.count("http:")
            j=words.count("https:")
            k=i+j
            url_count.append(k)
        return np.mean(url_count)

    def avg_urls_all(all_tweets):
        c=avg_urls_signal(all_tweets)
        return c

    def avg_hashtags_signal_tweet(signal_tweets):
        c=[]
        for each in signal_tweets:
            texts=each['text']
            s=re.findall('(?<=^|(?<=[^a-zA-Z0-9-\.]))#([A-Za-z]+[A-Za-z0-9_]+)',texts)
            no_of_hash=len(s)
            c.append(no_of_hash)
        return np.mean(c)

    def avg_hahstags_all_tweets(all_tweets):
        a=avg_hashtags_signal_tweet(all_tweets)
        return a

    def avg_usernames_signal_tweet(signal_tweets):
        c=[]
        for each in signal_tweets:
            texts=each['text']
            s=re.findall('(?<=^|(?<=[^a-zA-Z0-9-\.]))@([A-Za-z]+[A-Za-z0-9_]+)',texts)
            no_of_hash=len(s)
            c.append(no_of_hash)
        return np.mean(c)

    def avg_usernames_all_tweets(all_tweets):
        a=avg_usernames_signal_tweet(all_tweets)
        return a

    def statistical_features(all_tweets,signal_tweets):
        f1=ratio_signal_all(all_tweets,signal_tweets)
        f2=ratio_entr_word_freq(all_tweets,signal_tweets)
        f3=avg_no_words_signal(signal_tweets)
        f4=avg_no_words_alltweets(all_tweets)
        f5=rat_avg_words(signal_tweets,all_tweets)
        f6=perc_retweet_signal(signal_tweets)
        f7=perc_retweet_alltweets(all_tweets)
        f8=avg_urls_signal(signal_tweets)
        f9=avg_urls_all(all_tweets)
        f10=avg_hashtags_signal_tweet(signal_tweets)
        f11=avg_hahstags_all_tweets(all_tweets)
        f12=avg_usernames_signal_tweet(signal_tweets)
        f13=avg_usernames_all_tweets(all_tweets)
        return [f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13]
    return statistical_features(all_tweets,signal_tweets)
