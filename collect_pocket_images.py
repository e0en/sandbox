#!coding=utf-8
import sys
import os
import time
import requests
import pocket
import twitter

from private.keys import *


TAG = sys.argv[1]

# twitter api info
if not os.path.exists('private/.twitter_credentials'):
    twitter.oauth_dance("e0en's image downloader", twitter_consumer_key,
                        twitter_consumer_secret, '.twitter_credentials')
oauth_token, oauth_secret = twitter.read_token_file('.twitter_credentials')
twitter_instance = twitter.Twitter(
    auth=twitter.OAuth(oauth_token, oauth_secret, twitter_consumer_key,
                       twitter_consumer_secret))
twitter_api_url = 'https://api.twitter.com/1.1/statuses/show.json'


if access_token is None:
    # get a request token
    url = 'https://getpocket.com/v3/oauth/request'
    payload = {'consumer_key': consumer_key, 'redirect_uri': redirect_uri, }
    response = requests.post(url, payload)
    request_token = response.text.split('=')[1]

    # authorize my app on browser
    url = (
        'https://getpocket.com/auth/authorize?request_token=%s&redirect_uri=%s' %
        (request_token, redirect_uri))
    print('please open this url on your browser')

    # obtain access token
    url = 'https://getpocket.com/v3/oauth/authorize'
    payload = {'consumer_key': consumer_key, 'code': request_token, }
    response = requests.post(url, payload)
    access_token = response.text.split('=')[1]
    print(access_token)
else:
    instance = pocket.Pocket(consumer_key, access_token)
    items = instance.get(tag=TAG, since=0, state='all')[0]['list']
    for item_id in items:
        item_url = items[item_id]['resolved_url']
        # download from twitter only.
        if item_url.split('//')[1].startswith('twitter.com'):
            tweet_id = item_url[10:].split('/')[3]
            try:
                result = twitter_instance.statuses.show(_id=int(tweet_id))
                images = result['entities']['media']
                for x in images:
                    image_url = x['media_url_https']
                    filename = 'twitter_%s_%s' % (tweet_id,
                                                  image_url.split('/')[-1])
                    r_image = requests.get(image_url, stream=True)
                    with open(filename, 'wb') as fp:
                        fp.write(r_image.raw.read())
                    print(image_url)
                    print('downloaded %s' % filename)
                    time.sleep(0.1)

            except twitter.api.TwitterHTTPError:
                print('failed to retrieve %s' % item_url)
        else:
            print('skipping %s' % item_url)
