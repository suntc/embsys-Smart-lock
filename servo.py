'''
Created on 2016-06-19e
'''

#!/usr/bin/env python


import RPi.GPIO as GPIO
import time
import signal
import atexit

class servo:
    def __init__(self, pin=23):
        self.opened = True
        atexit.register(GPIO.cleanup)
        servopin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(servopin, GPIO.OUT, initial=False)
        self.p = GPIO.PWM(servopin,50) #50HZ
        self.p.start(0)
        #time.sleep(2)

    def open(self):
        print "open lock"
        if self.opened:
            for i in range(0,181,30):
                self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
                time.sleep(0.02)
                self.p.ChangeDutyCycle(0)
                time.sleep(0.2)
                self.opened = False
            return
        for i in range(181,0,-30):
            self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
            time.sleep(0.02)
            self.p.ChangeDutyCycle(0)
            time.sleep(0.2)
        self.opened = True

    def close(self):
        if not self.opened:
            for i in range(181,0,-30):
                self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
                time.sleep(0.02)
                self.p.ChangeDutyCycle(0)
                time.sleep(0.2)
                self.opened = True
            return
        print "close lock"
        for i in range(0,181,30):
            self.p.ChangeDutyCycle(2.5 + 10 * i / 180)
            time.sleep(0.02)
            self.p.ChangeDutyCycle(0)
            time.sleep(0.2)
        self.opened = False

if __name__ == '__main__':
    sv = servo()
    while True:
        raw_input()
        sv.close()
        raw_input()
        sv.open()
