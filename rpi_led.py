#!/usr/bin/env python
# -*- coding: utf-8 -*-
import RPi.GPIO as GPIO
import time


def blink(pin_number, n_blink, frequency):
    t_wait = 0.5 / frequency
    for _ in xrange(n_blink):
        GPIO.output(pin_number, True)
        time.sleep(t_wait)
        GPIO.output(pin_number, False)
        time.sleep(t_wait)


if __name__ == '__main__':
    GPIO.cleanup()
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(3, GPIO.OUT)
    blink(3, 100, 10)
    GPIO.cleanup()
