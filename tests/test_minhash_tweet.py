import pytest

from minhash2 import *
#test-case1
def test_gen_minhash_tweet1():
    """Check whether the function is generating a minhash"""
    sent="a"
    assert minhash(sent)==81314
    
def test_gen_minhash_tweet2():
    """Check whether the function is generating a minhash"""
    sent="generate a sentence"
    assert minhash(sent)==45364

def test_gen_minhash_tweet3():
    """Check whether the function is generating a minhash"""
    sent="i"
    assert minhash(sent)==73763
    
