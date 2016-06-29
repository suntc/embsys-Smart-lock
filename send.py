#!/usr/bin/python
#coding=utf8
# File Name: send.py
# Author: Wang Bo
# mail: zvcdx@qq.com
# Created Time: Tue 14 Jun 2016 01:00:51 PM CST

from threading import Thread

import serial
from time import sleep

class simcard_task(Thread):
    def __init__(self, token, phone):
        Thread.__init__(self)
        self.t = 0.2
        self.token = token
        self.phone = phone

    def run(self):
        print "send text message"
        info='Please use the following QRCode to fetch your package : )\r\n'
        ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=0.5)
        ser.write('AT\r')
        sleep(self.t)
        ser.write('AT+CMGF=1\r')
        sleep(self.t)
        ser.write('AT+CMGS="' + self.phone + '"\r')
        sleep(self.t)
        ser.write(info + "http://lo.wows.tech/qrcode/?data=" + self.token)
        sleep(self.t)
        ser.write('\x1A')
        sleep(self.t)
        ser.close()
