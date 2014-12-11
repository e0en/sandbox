#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
from datetime import datetime

import RPi.GPIO as GPIO

from private import EC2_URL


def send_status(status_id):
    time_str = datetime.utcnow().isoformat()
    url = EC2_URL + ('/register/%d/%s' % (status_id, time_str))
    print url
    urllib2.urlopen(url)


def is_locked(channel):
    return GPIO.input(channel)


def print_msg(channel):
    if is_locked(channel):
        send_status(0)
    else:
        send_status(1)


if __name__ == '__main__':
    print 'Sending switch status to %s' % EC2_URL

    channel = 29

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    is_locked(channel)

    GPIO.add_event_detect(channel, GPIO.BOTH, callback=print_msg)
    while True:
        pass

    GPIO.cleanup()
