import pytest

from rumorly import is_signal_tweet


#Test-Case1
def test_is_signal_tweet_isittrue():
    """Check whether the statement is a signal_tweet"""
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True



#Test-Case2

def test_is_signal_tweet_isis_itisrumor():
    """Check whether the statement is a signal_tweet"""
    t1="is it is a rumor"
    assert is_signal_tweet(t1)==True


#Test-Case3
def test_is_signal_tweet_not_isis():
    """Check whether the statement is a signal_tweet"""
    t1="isis"
    assert is_signal_tweet(t1)==False

#Test-Case4
def test_is_signal_tweet_whattt():
    """Check whether the statement is a signal_tweet"""
    t1="whattttttt? Is that true?"
    assert is_signal_tweet(t1)==True

#Test-case5
def test_is_signal_tweet_itisnottrue():
    """Check whether the statement is a signal_tweet"""
    t1="it is not true"
    assert is_signal_tweet(t1)==True
#test-case6
def test_is_signal_tweet_not_realize():
    """check whether statement is a signal_tweet"""
    t1="realize"
    assert is_signal_tweet(t1)==False
