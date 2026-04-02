# -*- coding: utf-8 -*-
"""
Python class for SIM922 modules installed in the SRS-SIM900 mainframe.
A device reference to the SIM900 mainframe should be initialised and passed as one of the
arguments. If none is given, a new one is created, but this should be avoided if possible.

message delivery system. Serial commands are sent after channel address corresponding to 
<slot number> on the mainframe. If a query is sent, response from module is written to the
mainframe buffer and read by invoking the SIM900.getmsg command (see mySIM900.py for details)

Serial commands provided by SRS, NB: CASE sensitive and do not pass parentheses []

+IDN?           Query module IDN string

+TVAL? c [,n]   Query the sensor temperature for channel c.

                If c=0, then all four channels are returned in the format:
                <c1>,<c2>,<c3>,<c4>
                If the optional parameter n is provided then n sequential conversion results 
                are returned to the host. If n=0, the conversion results continue indefinitely.
                To terminate the stream before n results (or when n=0), issue the SOUT command.
                Note that omitting n is equivalent to n=1.

SOUT            Stop streaming. 

                Turn off streaming output


======== REMAINING QUESTION(S) =========
1. What do the first 4 numbers proceeding # in the return string mean?
 - Not always the same for each routine, possibly depends on module(s)
 - SIM922 also returns a 4 integer value after #
 - Final digits looks to be counting the length of return string?
2. What is the voltage query parameter returning?
 - When should high/low gain be toggled?
 - Can this be used to determine latch event(s)? 

 Things to do:
 Change this object so that you pass through the reference for the mainframe once, and simply define
 the routines and channel numbers as many times as needed
"""

import sys, os, string, time, math

class Temp:
    def __init__(self, simRef, channel):
        # connect to mainframe and reference its location as meter
        self.meter = simRef
        if self.meter.idn['device'] != 'SIM900':
            print('Device reference did not identify as valid SIM900 mainframe. Trying default...')
            try:
                import mySIM900
                self.meter = mySIM900.Device('dev2')
                self.channel = int(channel)
                self.idn = self.get_idn()
            except:
                print('Device connection failed.')
                print('Please retry and connect to SIM900 first.')

        else:
            self.channel = int(channel)
            self.idn = self.get_idn() # store identifier for the SIM922 module


    def get_idn(self):
        # query module identifier and format into readable dictionary
        self.meter.write(self.channel, '*IDN?')
        #print(self.channel)
        retval = self.meter.getmsg(self.channel)
        #print(retval)
        interp = retval.split(',')
        #print(interp)
        idn = dict()
        idn['manufacturer'] = str(interp[0])
        idn['device'] = str(interp[1])
        idn['s/n'] = str(interp[2][2::])
        idn['version'] = str(interp[3][2::])
        return idn

    def get_temps(self):
        # query temperature of all sensors in Kelvin
        get_temp_cmd = 'TVAL? 0'
        self.meter.write(self.channel, str(get_temp_cmd))
        #read result from device
        time.sleep(0.5)
        raw_result = self.meter.getmsg(self.channel)
        #print('raw_result', raw_result)
        trim_result = raw_result[5::]
        #print('trim_result', trim_result)
        #split by commas
        result = trim_result.split(',')
        #convert to float
        temps = []
        for temp in result:
            temps.append(float(temp))
        return temps





    
if __name__ == '__main__':
    import mySIM900
    sim900 = mySIM900('dev2')
    temp1 = Temp(sim900,9) # SIM922 is installed in slot 9 (remote) of SIM900
    id = temp1.get_idn()
    print(id)
    temps = temp1.get_temps()
    print('Temperatures (K)', temps)