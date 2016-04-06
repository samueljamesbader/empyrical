# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:31:33 2016

@author: Samuel James Bader (samuel.james.bader@gmail.com)
"""

import win32com.client
import pythoncom
from threading import Thread, Lock
import time
import logging

class Horiba_iHR320:
    def __init__(self,instrument_id):
        '''http://stackoverflow.com/a/27966218'''
        self._closed=False
        logging.info("Initializing Horiba_iHR320 "+instrument_id+" ...")
        pythoncom.CoInitialize()
        labview=win32com.client.Dispatch("Labview.Application")
        self._lv_id=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, labview)
        self._lv_id_lock=Lock()
        self._instrument_id=instrument_id
        def runVI():
            self._lv_id_lock.acquire()
            pythoncom.CoInitialize()
            labview=win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(self._lv_id,pythoncom.IID_IDispatch))
            self._lv_id=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, labview)
            self._lv_id_lock.release()
            
            mc=labview.getvireference(r"C:\Users\Faria\Documents\Sam\TestingLabView\MonoControl.vi")
            time.sleep(3)
            mc.OpenFrontPanel
            mc.Run
            
        self._thread=Thread(target=runVI)
        self._thread.start()
        
    
    def close(self):
        if not self._closed:
            self._closed=True
            logging.info("Closing Horiba_iHR320 "+self._instrument_id)
            try: self._connect_thread()
            except: pass
            self._mc.Abort
            self._mc.CloseFrontPanel
            self._thread.join()
        
    def __enter__(self):
        return self
    def __exit__(self,*args,**kwargs):
        try:
            self._connect_thread()
        except:
            print('oops')
        self.close()

    def _connect_thread(self):
        self._lv_id_lock.acquire()
        pythoncom.CoInitialize()
        labview=win32com.client.Dispatch(pythoncom.CoGetInterfaceAndReleaseStream(self._lv_id,pythoncom.IID_IDispatch))
        self._lv_id=pythoncom.CoMarshalInterThreadInterfaceInStream(pythoncom.IID_IDispatch, labview)
        self._lv_id_lock.release()
        self._mc=labview.getvireference(r"C:\Users\Faria\Documents\Sam\TestingLabView\MonoControl.vi")
        

    def connect(self):
        self._connect_thread()
        time.sleep(1)
        self._mc.SetControlValue("Mono ID",self._instrument_id)
        self._mc.SetControlValue("Connect",True)
        time.sleep(5)
        self._mc.SetControlValue("Connect",False)
        logging.info("Horiba_iHR320 "+self._instrument_id+" ready.")
    
    @property
    def wavelength(self):
        return self._mc.GetControlValue("Current WL")
    @wavelength.setter
    def wavelength(self,wl):
        self._mc.SetControlValue("Target WL",wl)
        self._mc.SetControlValue("Move To\nTarget Positions",True)
        time.sleep(.1)
        self._mc.SetControlValue("Move To\nTarget Positions",False)
        logging.info("Waiting for move...")
        time.sleep(10)
        logging.info("Done waiting.")
        
    @property
    def grating(self):
        return self._mc.GetControlValue("Current Grating")
    @grating.setter
    def grating(self,gr):
        raise Exception("Set the grating_index, not the grating.")
        
    @property
    def grating_index(self):
        return self._mc.GetControlValue("Grating Index")
    
    @grating_index.setter
    def grating_index(self,gri):
        self._mc.SetControlValue("Target Grating",gri)
        self._mc.SetControlValue("Move To\nTarget Positions",True)
        time.sleep(.1)
        self._mc.SetControlValue("Move To\nTarget Positions",False)
        logging.info("Waiting for grating switch...")
        time.sleep(120)
        logging.info("Done waiting.")