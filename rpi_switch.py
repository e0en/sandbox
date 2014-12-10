#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import RPi.GPIO as GPIO

from private import EC2_URL


def send_status(status_id):
    url = EC2_URL + ('/register/%d' % status_id)
    urllib2.urlopen(url)


def is_locked(channel):
    return GPIO.input(channel)


def print_msg(channel):
    if is_locked(channel):
        send_status(0)
        print 'Door Locked'
    else:
        send_status(1)
        print 'Door Open'


if __name__ == '__main__':
    print 'Sending switch status to %s' % EC2_URL

    channel = 29

    is_locked(channel)

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(channel, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(channel, GPIO.BOTH, callback=print_msg)

    while True:
        pass

    GPIO.cleanup()
