#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import time
import traceback

import requests
from bs4 import BeautifulSoup

from private.keys import PUSHBULLET_TOKEN, PUSHBULLET_DEVICE_IDEN


def send_pushbullet(msg, token, device_iden):
    push_url = 'https://api.pushbullet.com/v2/pushes'
    headers = {
        'Access-Token': token,
        'Content-Type': 'application/json',
    }

    params = {
        'device_iden': device_iden,
        'type': 'note',
        'title': 'Parcel Update!',
        'body': msg,
    }

    return requests.post(push_url, headers=headers, json=params)


try:
    with open('/tmp/parcel_last_msg.txt') as fp:
        last_time, last_msg = fp.read().strip().split('\t')
        print('last_msg = ' + last_msg)
except:
    print(traceback.format_exc())
    last_msg = None
    last_time = '0.0'


parcel_num = sys.argv[1]
url = f'https://ilogen.com/mobile/trace_r.asp?gubun=slipno&value1={parcel_num}'
resp = requests.get(url)
resp.encoding = 'euc-kr'

print('URL: ' + url)

if not resp.ok:
    print(f'failed with HTTP {resp.status_code}')

soup = BeautifulSoup(resp.text, 'html.parser')

result_table = soup.find_all('table')[6]
result_rows = result_table.find_all('tr')[2:]
newest_item = result_rows[-1].text.strip()

print('current msg = ' + newest_item)

if newest_item == last_msg:
    print('No update :(')
    exit(0)

try:
    send_pushbullet(f'{newest_item}\n{url}',
                    PUSHBULLET_TOKEN, PUSHBULLET_DEVICE_IDEN)
    if resp.ok:
        now = time.time()
        with open('/tmp/parcel_last_msg.txt', 'w') as fp:
            fp.write(f'{now}\t{newest_item}')
    else:
        print(f'failed with HTTP {resp.status_code}')
except:
    print(traceback.format_exc())
