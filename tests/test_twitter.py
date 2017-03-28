import json

import pytest

from rumourly import twitter

stream  = twitter.STREAMING_API(key=1, payload={})

tweets = []
for idx, tweet in enumerate(stream.run()):
    tweets.append(tweet)

assert len(tweets) > idx
# inspect tweets
#print(json.dumps(tweet))
