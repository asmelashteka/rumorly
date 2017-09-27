import json

import pytest

from rumorly import twitter


def test_sample_stream():
    stream  = twitter.STREAMING_API(key=1, payload={})
    tweets = []
    for idx, tweet in enumerate(stream.run()):
        print(tweet)
        tweets.append(tweet)
        if idx == 10: break

    assert len(tweets) > idx
    # inspect tweets
    for tweet in tweets:
        print(json.dumps(tweet))



def test_filter_stream():
    stream  = twitter.STREAMING_API(key=1, payload={'hashtags':'rt'}, end_point='filter')
    tweets = []
    for idx, tweet in enumerate(stream.run()):
        print(tweet)
        tweets.append(tweet)
        if idx == 10: break

    assert len(tweets) > idx
    # inspect tweets
    for tweet in tweets:
        print(json.dumps(tweet))
