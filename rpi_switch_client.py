#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from datetime import datetime
import time

import RPi.GPIO as GPIO

from private import EC2_URL


def send_status(channel):
    status_id = 0 if is_locked(channel) else 1

    # TODO: handle server/network errors
    time_str = datetime.utcnow().isoformat()
    url = EC2_URL + ('/register/%d/%s' % (status_id, time_str))
    print url
    urllib2.urlopen(url)


def is_locked(channel):
    return GPIO.input(channel)


def send_alive():
    time_str = datetime.utcnow().isoformat()
    url = EC2_URL + ('/client_alive/%s' % time_str)
    urllib2.urlopen(url)

if __name__ == '__main__':
    print 'Sending switch status to %s' % EC2_URL

    channel = 29

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    send_status(channel)
    send_alive()

    GPIO.add_event_detect(channel, GPIO.BOTH, callback=send_status)
    while True:
        time.sleep(30)
        # TODO: send alive-message every minute
        send_alive()

    GPIO.cleanup()
