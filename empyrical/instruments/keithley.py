# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:34:05 2016

@author: Samuel James Bader (samuel.james.bader@gmail.com)
"""
import visa
import logging
class Keithley_2636A:
    '''
    Instrument driver for Keithley 2600-model Source Meter (tested with 2636A)
    '''
    def __init__(self, gpib_address=''):
        self._closed=False
        logging.info("Opening Keithley.")
        self._visa_handle = visa.ResourceManager().open_resource(gpib_address)
        self._visa_handle.read_termination = '\n'
    
    def close(self):
        if not self._closed:
            self._closed=True
            logging.info("Closing Keithley.")
            self.resetA()
            self.resetB()
            self._visa_handle.close()

    def __enter__(self):
        return self
    def __exit__(self,*args,**kwargs):
        self.close()
        
    @property
    def currentA(self):
        '''Get the current reading for channel A.'''
        return float(self._visa_handle.query('print(smua.measure.i())'))
    @property
    def currentB(self):
        '''Get the current reading for channel B.'''
        return float(self._visa_handle.query('print(smub.measure.i())'))
    @currentA.setter
    def currentA(self, value):
        '''Set the source current for channel A.'''
        self._visa_handle.write('smua.source.func=smua.OUTPUT_DCAMPS;smua.source.leveli=%s' % value)
    @currentB.setter
    def currentB(self, value):
        '''Set the source current for channel B.'''
        self._visa_handle.write('smub.source.func=smub.OUTPUT_DCAMPS;smub.source.leveli=%s' % value)

    @property
    def voltageA(self):
        '''Get the voltage reading for channel A'''
        return float(self._visa_handle.query('print(smua.measure.v())'))
    @property
    def voltageB(self):
        '''Get the voltage reading for channel B'''
        return float(self._visa_handle.query('print(smub.measure.v())'))
    @voltageA.setter
    def voltageA(self, value):
        '''Set the source voltage for channel A.'''
        self._visa_handle.write('smua.source.func=smua.OUTPUT_DCVOLTS;smua.source.levelv=%s' % value)
    @voltageB.setter
    def voltageB(self, value):
        '''Set the source voltage for channel B.'''
        self._visa_handle.write('smub.source.func=smub.OUTPUT_DCVOLTS;smub.source.levelv=%s' % value)

    @property
    def modeA(self):
        '''Get the source function for channel A.'''
        return self._visa_handle.query('print(smuA.source.func())')
    @property
    def modeB(self):
        '''Get the source function for channel B.'''
        return self._visa_handle.query('print(smuB.source.func())')
    @modeA.setter
    def modeA(self, value):
        '''Set the source function ('voltage' or 'current') for channel A'''
        value={'voltage':'OUTPUT_DCVOLTS','current':'OUTPUT_DCAMPS'}[value]
        self._visa_handle.write('smua.source.func=smua.%s' % value)
    @modeB.setter
    def modeB(self, value):
        '''Set the source function ('voltage' or 'current') for channel B'''
        value={'voltage':'OUTPUT_DCVOLTS','current':'OUTPUT_DCAMPS'}[value]
        self._visa_handle.write('smub.source.func=smub.%s' % value)

    @property
    def outputA(self):
        '''Gets the source output ('on'/'off'/'highz') for channel A'''
        return {0: 'off', 1:'on', 2: 'highz'}[int(float(self._visa_handle.query('print(smua.source.output)')))]
    @property
    def outputB(self):
        '''Gets the source output ('on'/'off'/'highz')  for channel B'''
        return {0: 'off', 1:'on', 2: 'highz'}[int(float(self._visa_handle.query('print(smub.source.output)')))]
    @outputA.setter
    def outputA(self, value):
        '''Sets the source output ('on'/'off'/'highz') for channel A'''
        status = 'ON' if ((value==True) or (value==1) or (value=='on')) else 'OFF'
        self._visa_handle.write('smua.source.output= smua.OUTPUT_%s' %status)
    @outputB.setter
    def outputB(self, value):
        '''Sets the source output ('on'/'off'/'highz') for channel B'''
        status = 'ON' if ((value==True) or (value==1) or (value=='on')) else 'OFF'
        self._visa_handle.write('smub.source.output= smub.OUTPUT_%s' %status)

    @property
    def voltagelimitA(self):
        '''Get the output voltage compliance limit for channel A'''
        return float(self._visa_handle.query('print(smua.source.limitv'))
    @property
    def voltagelimitB(self):
        '''Get the output voltage compliance limit for channel B'''
        return float(self._visa_handle.query('print(smub.source.limitv'))
    @voltagelimitA.setter
    def voltagelimitA(self,value):
        '''Get the output voltage compliance limit for channel A'''
        return self._visa_handle.write('smua.source.limitv=%s' %value)
    @voltagelimitB.setter
    def voltagelimitB(self,value):
        '''Get the output voltage compliance limit for channel B'''
        return self._visa_handle.write('smub.source.limitv=%s' %value)


    @property
    def currentlimitA(self):
        '''Get the output current compliance limit for channel A'''
        return float(self._visa_handle.query('print(smua.source.limiti'))
    @property
    def currentlimitB(self):
        '''Get the output current compliance limit for channel B'''
        return float(self._visa_handle.query('print(smub.source.limiti'))
    @currentlimitA.setter
    def currentlimitA(self,value):
        '''Get the output current compliance limit for channel A'''
        return self._visa_handle.write('smua.source.limiti=%s' %value)
    @currentlimitB.setter
    def currentlimitB(self,value):
        '''Get the output current compliance limit for channel B'''
        return self._visa_handle.write('smub.source.limiti=%s' %value)
        
    @property
    def sensemodeA(self,value):
        '''Gets the source output ('on'/'off'/'highz') for channel A'''
        return {0: '2-wire', 1:'4-wire', 2: 'cal'}[int(float(self._visa_handle.query('print(smua.sense)')))]
    @property
    def sensemodeB(self,value):
        '''Gets the source output ('on'/'off'/'highz') for channel B'''
        return {0: '2-wire', 1:'4-wire', 2: 'cal'}[int(float(self._visa_handle.query('print(smub.sense)')))]
    @sensemodeA.setter
    def sensemodeA(self,value):
        '''Get the output current compliance limit for channel A'''
        value={'2-wire':'0','4-wire':'1','cal':'2'}[value]
        return self._visa_handle.write('smua.sense=%s' %value)
    @sensemodeB.setter
    def sensemodeB(self,value):
        '''Get the output current compliance limit for channel A'''
        value={'2-wire':'0','4-wire':'1','cal':'2'}[value]
        return self._visa_handle.write('smub.sense=%s' %value)

    def resetA(self):
        '''Resets the A channel'''
        self._visa_handle.write('smua.reset()')
    def resetB(self):
        '''Resets the B channel'''
        self._visa_handle.write('smub.reset()')
