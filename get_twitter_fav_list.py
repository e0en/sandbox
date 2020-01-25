#!/usr/bin/env python
#!coding=utf-8
import sys
import os
import time
import requests
import twitter
import private.keys as pk


screen_name = sys.argv[1]
credential_file = 'private/.twitter_credentials'


# twitter api info
if not os.path.exists(credential_file):
    twitter.oauth_dance('test', pk.twitter_consumer_key,
                        pk.twitter_consumer_secret, credential_file)
oauth_token, oauth_secret = twitter.read_token_file(credential_file)
auth = twitter.OAuth(oauth_token, oauth_secret,
                     pk.twitter_consumer_key, pk.twitter_consumer_secret)
client = twitter.Twitter(auth=auth)

max_id = None
n_result = 0

while True:
    if max_id:
        resp = client.favorites.list(screen_name=screen_name, count=200, max_id=max_id)
        resp = resp[1:]
    else:
        resp = client.favorites.list(screen_name=screen_name, count=200)
    if not resp:
        break
    for tw in resp:
        n_result += 1
        tw_id = tw['id']
        print(tw_id)
    max_id = resp[-1]['id']
    time.sleep(1)
