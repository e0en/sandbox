#!/usr/bin/env python
# -*- coding: utf-8 -*-
import urllib2
import RPi.GPIO as GPIO

from private import EC2_URL


def print_msg(channel):
    try:
        if GPIO.input(channel):
            urllib2.urlopen(EC2_URL + '/register/0')
            print 'Door Locked'
        else:
            urllib2.urlopen(EC2_URL + '/register/1')
            print 'Door Open'
    except urllib2.HTTPError:
        print "Failed to push door status to server"


if __name__ == '__main__':
    print 'Sending switch status to %s' % EC2_URL

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(29, GPIO.BOTH, callback=print_msg)

    while True:
        pass

    GPIO.cleanup()
