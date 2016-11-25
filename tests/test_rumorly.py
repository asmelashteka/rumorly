import pytest

from rumorly import is_signal_tweet

def test_is_signal_tweet():
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True

