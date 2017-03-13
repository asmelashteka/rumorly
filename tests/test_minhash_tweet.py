import pytest

from minhash2 import *
#test-case1
def test_gen_minhash_tweet1():
    sent="a"
    assert minhash(sent)==81314
    
def test_gen_minhash_tweet2():
    sent="generate a sentence"
    assert minhash(sent)==45364

def test_gen_minhash_tweet3():
    sent="i"
    assert minhash(sent)==73763
    
