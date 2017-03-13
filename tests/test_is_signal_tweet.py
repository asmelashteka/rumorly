import pytest

from rumorly import is_signal_tweet


#TODO
"""
Change all your test suit such that
(i) there's a description of what's being tested
(ii) they are proper python scripts. i.e., one can type
pytest and see the test results.
Remove all output and report etc.

Below is an example for Test-case1

def test_name_exists():
    """one line description of what this test case is checking"""
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True

"""
#Test-Case1
def test_is_signal_tweet():
    """Check whether the statement contains signal pattern-is it true"""
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True



#Test-Case2

def test_is_signal_tweet():
    """Check whether the statement contains signal pattern-rumor"""
    t1="isis is a rumor"
    assert is_signal_tweet(t1)==True


#Test-Case3
def test_is_signal_tweet():
    """Check whether the statement contains signal pattern-is"""
    t1="isis"
    assert is_signal_tweet(t1)==True

#Test-Case4
def test_is_signal_tweet():
    """Check whether the statement contains signal pattern-what?"""
    t1="whattttttt? Is that true?"
    assert is_signal_tweet(t1)==True

#Test-case5
def test_is_signal_tweet():
    """Check whether the statement contains signal pattern-it is not true"""
    t1="it is not true"
    assert is_signal_tweet(t1)==True

