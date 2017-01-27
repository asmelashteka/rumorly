import pytest

from rumorly import is_signal_tweet


"Test-case1"
def test_is_signal_tweet():
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True
"output:   
C:\Users\JAYANTH\Desktop\proj>py.test test_is_signal_tweet.py
============================= test session starts =============================
platform win32 -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
rootdir: C:\Users\JAYANTH\Desktop\proj, inifile:
collected 1 items

test_is_signal_tweet.py .

========================== 1 passed in 1.15 seconds ===========================
"



"Test-Case2"
def test_is_signal_tweet():
    t1="isis is a rumor"
    assert is_signal_tweet(t1)==True
"output:
C:\Users\JAYANTH\Desktop\proj>py.test test_is_signal_tweet.py
============================= test session starts =============================
platform win32 -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
rootdir: C:\Users\JAYANTH\Desktop\proj, inifile:
collected 1 items
test_is_signal_tweet.py .

========================== 1 passed in 1.17 seconds ===========================
"


"Test-Case3"
def test_is_signal_tweet():
    t1="isis"
    assert is_signal_tweet(t1)==True
"output:
================================== FAILURES ===================================
____________________________ test_is_signal_tweet _____________________________

    def test_is_signal_tweet():
        t1="isis"
>       assert is_signal_tweet(t1)==True
E       assert False == True
E        +  where False = is_signal_tweet('isis')

test_is_signal_tweet.py:7: AssertionError
========================== 1 failed in 1.30 seconds ===========================
"


"Test-Case4"
def test_is_signal_tweet():
    t1="whattttttt? Is that true?"
    assert is_signal_tweet(t1)==True
    
"output:
C:\Users\JAYANTH\Desktop\proj>py.test test_is_signal_tweet.py
============================= test session starts =============================
platform win32 -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
rootdir: C:\Users\JAYANTH\Desktop\proj, inifile:
collected 1 items

test_is_signal_tweet.py .

========================== 1 passed in 1.15 seconds ===========================
"





"Test-case5"
def test_is_signal_tweet():
    t1="it is not true"
    assert is_signal_tweet(t1)==True

"output:
C:\Users\JAYANTH\Desktop\proj>py.test test_is_signal_tweet.py
============================= test session starts =============================
platform win32 -- Python 3.5.2, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
rootdir: C:\Users\JAYANTH\Desktop\proj, inifile:
collected 1 items

test_is_signal_tweet.py .

========================== 1 passed in 1.12 seconds ===========================
"






