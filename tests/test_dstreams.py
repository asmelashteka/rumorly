from queue import Queue
import time
import random

from rumorly import twitter
import pytest
import threading

tweets = Queue()
_sentinel = object()


def gen_dstreams(window=20):
    '''generates discrete tweet streams.
    simulates this by adding a sentinel at every window

    @param window in seconds
    '''
    start_time = time.time()
    stream = twitter.STREAMING_API(key=1, payload={})
    for tweet in stream.run():
        tweets.put(tweet)
        if int(time.time() - start_time) % window == 0:
            tweets.put(_sentinel)
            time.sleep(1)


def test_dstresm():
    t = threading.Thread(target=gen_dstreams)
    t.deamon = True
    t.start()
    epoch = 0
    while True:
        epoch += 1
        print('Epoch {}'.format(epoch))
        tweet_count = 0
        while True:
            tweet = tweets.get()
            tweet_count += 1
            #print('tweets count {}'.format(tweet_count))
            if tweet is _sentinel:
                break
        print('clustering for {} tweets'.format(tweet_count))
