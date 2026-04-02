# -*- coding: utf-8 -*-
"""
Python script to interface SIM900 mainframe over GPIB-USB connection from 
host PC. Primary methods write() and read() send commands to mainframe, an
internal messaging system routes commands for each module.

write() sends commands to the SIM900 mainframe. Command syntax begin with a 
4 character block followed by arguments, e.g.,  port number, values.
Line feed escape sequence \n terminates a message delivery and instructs the
module to execute all received commands.
Commands starting with * followed by 3 letters are IEEE 488.2 specific while
4 letters are reserved for SIM900, for information see SIM900 manual.

read() transfers all bits on mainframe buffer to host PC. In a typical 
routine the host PC must issue a delivery of message from a device at any
given port to the mainframe buffer. Only then can the host PC retrieve bits
relating to any query.

Port numbers:
SIM900 supports 9 SIM modules, 8 front bays and 1 remote connection via back.
Ports [1, 2, .., 9] are addressable if populated with appropriate module.
Auxillary ports [A, B, C, D] are unused in most cases.

Basics of operation:
To issue an instruction or query, write() is used to send a command to the
SIM900 mainframe. If wanting to issue a command to a specific module, use the
SNDT <SeND Terminated> command which 
"""

import sys, os, string, time
#from myGpib import *
from mySerial import serialSrs


class Device:
    def __init__(self, name, connection= 'gpib'):
        # connect to SIM900 using myGpib script using Gpib class defined in myGpib
        if connection == 'gpib':
            self.mframe = Gpib(name)
        elif connection == 'serial':
            self.mframe= serialSrs(name)
        else:
            raise ValueError('Connection type must be gpib or serial')
        # initialisation sequence: clear buffer, reset status flags, flush message queue
        self.mframe.write('*RST\n')
        self.mframe.write('SRST\n')
        self.mframe.write('FLSH\n')
        
        # check the IDN matches <Stanford_Research_Systems,SIM900,s/n130559,ver3.6>
        self.mframe.write('*IDN?\n')
        time.sleep(0.5)
        retval = self.mframe.read().decode("utf-8")
        interp = retval.split(',')
        if len(interp) == 4 and interp[0] == 'Stanford_Research_Systems':
            self.idn = dict()
            self.idn['manufacturer'] = interp[0]
            self.idn['device'] = interp[1]
            self.idn['s/n'] = interp[2]
            self.idn['version'] = interp[3]
            print('Success! Connected to %s %s mainframe' %(self.idn['manufacturer'].replace('_',' '), self.idn['device']))
        else:
            print('unexpected return identifier from device')
            print(interp)


    def write(self, chan, msg):
        # main function: SNDT <SeND Terminated> commands to SIM900
        outstring = 'SNDT %d,"%s"' %(chan, msg)
        self.mframe.write(outstring)
        time.sleep(0.1)


    def getmsg(self, chan):
        # retrieve message stored on buffer from specified slot
        leng = self.getninp(chan)
        self.mframe.write('GETN? %i,%i\n' %(chan, leng))
        time.sleep(0.1)
        retval = self.mframe.read().decode("utf-8")
        indx = retval.find('\n')
        msg = retval[0:indx]
        return msg

    def getninp(self, chan):
        # get <Number of INPut> bits awaiting delivery at port <chan>
        outstring = 'NINP? %d\r' %chan
        self.mframe.write(outstring)
        time.sleep(0.1)
        msg = self.mframe.read().decode('utf-8')
        if len(msg) >= 2:
            try:
                idx = msg.find('\n')
                leng = int(msg[0:idx])
            except:
                print('Exception, message', msg, len(msg))
                leng = -1
        return leng


    def getstatus(self, chan = None):
        # get status byte from mainframe
        if chan == None:
            self.mframe.write('SSCR?\r')
        else:
            self.mframe.write('SSCR? %d\r' %chan)
        time.sleep(0.1)
        return int(self.mframe.read().split()[0])


if __name__ == '__main__':
    sim900 = Device('dev2')
    for k in range(5):
        print(sim900.getstatus())
        time.sleep(1.0)
    sim900.mframe.close()