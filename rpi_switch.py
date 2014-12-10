#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO


def print_msg(channel):
    if GPIO.input(channel):
        print 'Door Locked'
    else:
        print 'Door Open'



if __name__ == '__main__':
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(29, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
    GPIO.add_event_detect(29, GPIO.BOTH, callback=print_msg)
    while True:
        pass

    GPIO.cleanup()
