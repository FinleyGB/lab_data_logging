# -*- coding: utf-8 -*-
"""
Script for communicating with SIM900 mainframe over Serial (RS-232 port).
Message delivery must be terminated, this is taken care of by including the
escape sequence, \r\n for each message string

Recall valid messages are 4 character upper-case, followed by a comma and 
the parameter
"""

import os, sys, serial, string


class serialSrs:

    def __init__(self, name='COM5'):

        self.meter = serial.Serial(port=name, baudrate=9600, timeout=1.0)
        #old_write = self.meter.write
        #new_write = lambda x: old_write(str(x).encode('utf-8'))
        #self.meter.write = new_write
        
        # clear output/input buffers on Serial bus
        self.meter.flushInput()
        self.meter.flushOutput()

        # clear output/input buffers on SRS mainframe
        self.meter.write("*RST\r".encode())
        self.meter.write('FLSH\r'.encode())

        # reset SIM module        
        self.meter.write('SRST\r'.encode())


    def close(self):
        # subroutine for closing connection to SIM900
        self.meter.close()


    def write(self, msg):
        # prepare message with termination
        self.meter.write((str(msg) + '\r\n').encode())


    def read(self, length=512):
        # read fixed length of 80 bytes from buffer
        # return self.meter.readline()
        return self.meter.read(length)

if __name__ =='__main__':
    print(serial)
    serial_device = serialSrs()
    serial_device.write('*IDN?\n')
    print(serial_device.read(512*8))