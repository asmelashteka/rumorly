import pytest

from rumorly import is_signal_tweet

def test_is_signal_tweet_isittrue():
    """Check whether the statement is a signal_tweet"""
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True


def test_is_signal_tweet_isis_itisrumor():
    """Check whether the statement is a signal_tweet"""
    t1="is it is a rumor"
    assert is_signal_tweet(t1)==True
    

def test_is_signal_tweet_isittrue_braces():
    t1="(is it true?)"
    assert is_signal_tweet(t1)==True

def test_is_signal_tweet_realize():
    t1="i realize it at the end"
    assert is_signal_tweet(t1)==False


def test_is_signal_tweet_brumor():
    t1="brumor"
    assert is_signal_tweet(t1)==False
    
def test_is_signal_tweet_disconfirmed():
    t1="disconfirmed"
    assert is_signal_tweet(t1)==False

def test_is_signal_tweet_really():
    t1="really"
    assert is_signal_tweet(t1)==False

def test_is_signal_tweet_debunked():
    t1="debunked"
    assert is_signal_tweet(t1)==True

def test_is_signal_tweet_rumors():
    t1="rumors"
    assert is_signal_tweet(t1)==True
    
def test_is_signal_tweet_what():
    t1="what"
    assert is_signal_tweet(t1)==False


def test_is_signal_tweet_what_quest():
    t1="what?"
    assert is_signal_tweet(t1)==True

def test_is_signal_tweet_what_exclam():
    t1="what!"
    assert is_signal_tweet(t1)==True

def test_is_signal_tweet_isis():
    t1="isis"
    assert is_signal_tweet(t1)==False
