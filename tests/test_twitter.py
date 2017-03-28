import json

import pytest

from rumorly import twitter

stream  = twitter.STREAMING_API(key=1, payload={})

def test_sample_stream():
    tweets = []
    for idx, tweet in enumerate(stream.run()):
        print(tweet)
        tweets.append(tweet)
        if idx == 10: break

    assert len(tweets) > idx
    # inspect tweets
    for tweet in tweets:
        print(json.dumps(tweet))
