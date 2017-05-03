import sys
import json
import time
import datetime
import logging
from queue import Queue
from threading import Thread

import requests
from requests_oauthlib import OAuth1

from .credentials import get_keys

_sentinel = object()

class _STREAM_TASK:
    """Wraps a stream to make it stoppable."""
    def __init__(self):
        self._running = True

    def terminate(self):
        logging.debug('Terminate running _STREAM_TASK...')
        self._running = False

    def run(self, stream, TWEETS):
        logging.debug('Inside Streaming task')
        logging.debug('Request code {}'.format(stream.status_code))
        while self._running:
            try:
                for tweet in stream.iter_lines():
                    if tweet: TWEETS.put(json.loads(tweet.decode('utf-8')))
            except:
                continue
        TWEETS.put(_sentinel)


class STREAMING_API():
    """Wrapper around Twitter streaming APIs."""
    def __init__(self, key, payload=None, end_point='sample'):
        self.key       = key
        self.end_point = end_point
        self.payload   = self._set_payload(payload)
        self.session   = self._set_session()
        self.stream    = _STREAM_TASK()
        self.TWEETS    = Queue()
        self._running  = True

    def run(self, keywords=None):
        logging.debug('Inside Streaming API')
        if keywords: self.payload['track'] = ','.join(keywords)
        api = self._get_api()
        t = Thread(target=self.stream.run, args=(api, self.TWEETS))
        t.start()
        while self._running:
            try:
                tweet = self.TWEETS.get()
                if tweet is _sentinel:
                    self.TWEETS.put(_sentinel)
                    break
                yield(tweet)
            except ValueError as e:
                e = sys.exc_info()[0]
                sys.stderr.write('{} {} {} {}\n'.format(
                    time.asctime(), str(e), self.end_point, self.key))
                raise

    def close(self):
        logging.debug('Close STREAMING_API...')
        self._running = False
        self.stream.terminate()

    def _set_session(self):
        keys = get_keys(self.key)
        s = requests.Session()
        s.auth = OAuth1(**keys)
        return s

    def _get_api(self):
        """Track semantics A comma-separated list of phrases
        e.g. 'the twitter' is the AND twitter, and 'the,twitter' is the OR twitter
        """
        if self.end_point == 'sample':
            url = 'https://stream.twitter.com/1.1/statuses/sample.json'
            return self.session.get(url, stream=True)

        elif self.end_point == 'filter':
            url = 'https://stream.twitter.com/1.1/statuses/filter.json'
            return self.session.post(url, data=self.payload, stream=True)

        elif self.end_point == 'search':
            url = 'https://stream.twitter.com/1.1/statuses/search.json'
            return self.session.post(url, data=self.payload, stream=True)

    def _set_payload(self, payload):
        """ STREAMING API request parameters
        https://dev.twitter.com/streaming/overview/request-parameters

        filter_level: one of none, low, or medium default is none
        language: a comma-separated list of BCP 47 language identifiers
        follow: a comma-separated list of user IDs
        track: a comma-separated list of phrases - one or more terms separated by spaces
        locations: a comma-separated list of longitude,latitude pairs
        replies: to have tweets mentioning a user that we don't follow
        """
        if payload.get('lang'):
            payload['language'] = payload.get('lang')
        if payload.get('language') == 'all':
            del payload['language']
        if payload.get('hashtags'):
            payload['track'] = payload.get('hashtags')
        if payload.get('location'):
            payload['locations'] = payload.get('location')
        fields = ['language', 'track', 'locations', 'filter_level', 'replies']
        return {k:v for k,v in payload.items() if k in fields}
