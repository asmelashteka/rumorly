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
"""


def test_name_exists():
    """one line description of what this test case is checking"""
    t1 = "Is it true that Obama found  a bomb?"
    assert is_signal_tweet(t1) == True

"""
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





"""
