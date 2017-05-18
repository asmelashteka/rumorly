# -*- coding: utf-8 -*-
import time
import os,sys
import itertools
import math
import argparse
import numpy as np
from multiprocessing import Pool
from hashlib import sha1
import random, struct
from random import sample,choice
from sklearn import metrics

def create_lsh(id_text_dict,no_of_perm,thr):
    M_PRIME = (1 << 89) - 1
    MAX_HASH = (1 << 64) - 1
    random.seed(427)
    A,B = np.array([(random.randint(1, M_PRIME),random.randint(0, M_PRIME)) for _ in range(no_of_perm)]).T
    mycorpus=[(ids,set(text.lower().split())) for ids,text in id_text_dict.items()]
    global hashcorp
    hashcorp=dict.fromkeys([tup[0] for tup in mycorpus])
    #####################################################################################################################################
    def get_permuted_hashes(token):
        hv=int(sha1(token.encode('utf-8')).hexdigest(),16)% (10 ** 12)
        return np.bitwise_and((A * hv + B) % M_PRIME,MAX_HASH)
    #####################################################################################################################################
    def get_lsh(sig,nbands):
        for i,band in enumerate(np.array_split(sig,nbands)):
            return sha1(("ab" + str(band) + "ba"+str(i)).encode('utf8')).digest()

    #####################################################################################################################################
    def get_bandwidth(n, thr):
        best = n, 1
        minerr  = float("inf")
        for r in range(1, n + 1):
            try:
                b = 1. / (thr ** r)
            except: 
                return best
            err = abs(n - b * r)
            if err < minerr:
                best = r
                minerr = err
        return best
    #####################################################################################################################################
    for key,doc in mycorpus:
        hashvalues=np.empty(no_of_perm)
        hashvalues.fill(MAX_HASH)
        for token in doc:
            hashvalues=np.minimum(get_permuted_hashes(token), hashvalues)
        hashcorp[key]=hashvalues
    bandwidth=get_bandwidth(no_of_perm, thr)
    bands=int(math.ceil(float(no_of_perm)/float(bandwidth)))
    doc_to_lsh={}
    lsh_dict={}
    for key,m in hashcorp.items():
        signatures = [sig for sig in get_lsh(m,bands)]
        doc_to_lsh[key]=signatures
        for sig in signatures:
            if sig in lsh_dict:
                lsh_dict[sig].append(key)
            else:
                lsh_dict[sig]=[key]
    return lsh_dict,doc_to_lsh,hashcorp


def jaccard(h1,h2):
    return np.float(np.count_nonzero(h1==h2)) /np.float(h2.size)

def connected(seed,lshdict,doc2lsh,t):
    cluster=set([seed])
    base=set([seed])
    while len(base)>0:
        s=base.pop()
        candidates=set(itertools.chain.from_iterable([lshdict[sig] for sig in doc2lsh[s]]))
        m1=hashcorp[s]
        for cand in candidates:
            if cand in cluster:continue
            m2=hashcorp[cand]
            if jaccard(m1,m2) >=t:
                cluster.add(cand)
                base.add(cand)
    return cluster

def near_duplicates(seed,lshdict,doc2lsh,t):
    cluster=set([seed])
    #get candidates and flatten list
    candidates=set(itertools.chain.from_iterable([lshdict[sig] for sig in doc2lsh[seed]]))
    m1=hashcorp[seed]
    for cand in candidates:
        if cand in cluster:continue#don't check if we've already added this
        m2=hashcorp[cand]
        if jaccard(m2,m1) >=t:
            cluster.add(cand)
    #all candidates have been checked  
    return cluster

def create_clusters(lsh_dict,doc_to_lsh,hashcorp,thr):
    doc2cluster={}
    count=0
    for doc in hashcorp:
        if doc not in doc2cluster:
            cl=connected(doc,lsh_dict,doc_to_lsh,thr)
            doc2cluster.update({i:count for i in cl })
            count+=1
    final={}
    for val in doc2cluster:
        if doc2cluster[val] in final:
            final[doc2cluster[val]].append(val)
        else:
            final[doc2cluster[val]]=[val]
    final_clusters={}
    for keys,values in final.items():
        if len(values)>3:
            final_clusters.update({keys:values})
    return final_clusters


