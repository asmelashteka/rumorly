from collections import Counter
import sys
non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)

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
    sent=[]
    sent= ' '.join(words_list)

    return sent


a=extract_summary({'there is a plane crash in atlantic','is is true that there is a plane crash',
                  'i have seen the plane crash'})

        
b=extract_summary({'airwings flight has crashed in alps','is it true that airwings plane from dusseldorf has crashed?','breaking:airplane crashed in apls'})

print(a)
print(b)
