#!coding=utf-8
import sys
import os
import time
import requests
import twitter
import private.keys as pk
from pprint import pprint


tweet_id = sys.argv[1]
credential_file = 'private/.twitter_credentials'


# twitter api info
if not os.path.exists(credential_file):
    twitter.oauth_dance('test', pk.twitter_consumer_key,
                        pk.twitter_consumer_secret, credential_file)
oauth_token, oauth_secret = twitter.read_token_file(credential_file)
auth = twitter.OAuth(oauth_token, oauth_secret,
                     pk.twitter_consumer_key, pk.twitter_consumer_secret)
client = twitter.Twitter(auth=auth)

result = client.statuses.show(_id=int(tweet_id), include_entities=True,
                             tweet_mode='extended')
pprint(result)
