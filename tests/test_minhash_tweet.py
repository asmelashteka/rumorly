import pytest

from rumorly import *
#test-case1
def test_gen_minhash_tweet1():
    #check whether the function generates a minhash
    sent="a"
    tweet_id=232444
    assert minhash(sent,tweet_id,signal_minhashes,lsh_signal) in signal_minhashes.values()
    

    
def test_gen_minhash_tweet2():
    #check whether the function generates a minhash
    sent="there is a accident in washington"
    tweet_id=83746464
    assert minhash(sent,tweet_id,signal_minhashes,lsh_signal) in signal_minhashes.values()

def test_gen_minhash_tweet3():
    #check whether the function generates a minhash
    sent="876577655446788"
    tweet_id=6557767
    assert minhash(sent,tweet_id,signal_minhashes,lsh_signal) in signal_minhashes.values()

def test_gen_minhash_tweet4():
    #check whether the function generates a minhash and index the minhash in lsh
    sent="hello braunschweig how are you"
    tweet_id=9849385359
    minhash(sent,tweet_id,signal_minhashes,lsh_signal)
    assert "9849385359" in lsh_signal

def test_gen_minhash_tweet5():
    #check whether the function generates a minhash and index the minhash in lsh
    sent="berlin is a vibrant city"
    tweet_id=9666050667
    minhash(sent,tweet_id,signal_minhashes,lsh_signal)
    assert "9666050667" in lsh_signal
