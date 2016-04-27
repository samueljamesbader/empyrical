# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 21:26:23 2016

@author: Samuel James Bader (samuel.james.bader@gmail.com)
"""
import os.path
import logging
import imp
import time

class LogManager:
    def __init__(self,expname,datacols,datawidth=20):
        self._closed=False
        if not os.path.exists("Data"):
            os.makedirs("Data")
        if not os.path.exists("Log"):
            os.makedirs("Log")
        
        date=time.strftime('%Y-%m-%d')
        ts=time.strftime('%H-%M-%S')
        
        datadir=os.path.join("Data",date)
        if not os.path.exists(datadir):
            os.makedirs(datadir)
        self._dataname=os.path.join(datadir,expname+"_"+date+"_"+ts+".csv")
        
        logdir=os.path.join("Log",date)
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        self._logname=os.path.join(logdir,expname+"_"+date+"_"+ts+".log")
        
        self._datacols=datacols
        self._datawidth=datawidth
        
        
        imp.reload(logging) # http://stackoverflow.com/a/18809051
        logging.basicConfig(filename=self._logname,
            level=logging.INFO,
            format='%(asctime)s %(message)s')
        
        class MyHandler(logging.Handler):
            def emit(self, record):
                print(record.message)
                
        toconsole=MyHandler()
        toconsole.setLevel(level=logging.INFO)
        
        logging.getLogger().addHandler(toconsole)
        
        self._data=open(self._dataname,'w')
        self._headers_out=False
        
    
    def close(self):
        if not self._closed:
            self._closed=True
            self._data.close()
            logging.shutdown()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        self.close()
    
    
    def output_headers(self):        
        headerprep=(lambda h: h.rjust(self._datawidth))\
            if self._datawidth is not None else (lambda h: h)
        self._data.write(",".join([headerprep(d[0])
            for d in self._datacols])+"\n")
        self._headers_out=True
                
    def output_data(self,data):
        assert len(data)==len(self._datacols), "Wrong number of data reported."
        if not self._headers_out:
            self.output_headers()
        data=[f.format(d) for d,(n,f) in zip(data,self._datacols)]
        if self._datawidth is not None:
            data=[d.rjust(self._datawidth) for d in data]
        self._data.write(",".join(data)+"\n")
        
    def output_comment(self,comment):
        if not self._headers_out:
            self.output_headers()
        self._data.write("#"+comment+"\n")
        
    def debug(self,*args,**kwargs):
        return logging.debug(*args,**kwargs)
    def info(self,*args,**kwargs):
        return logging.info(*args,**kwargs)
    def warning(self,*args,**kwargs):
        return logging.warning(*args,**kwargs)
    def error(self,*args,**kwargs):
        return logging.error(*args,**kwargs)
    def critical(self,*args,**kwargs):
        return logging.critical(*args,**kwargs)
        
    def get_logname(self):
        return self._logname
    def get_dataname(self):
        return self._dataname
        
        
        
class FakeLogManager:
    def __init__(self,expname,datacols,datawidth=20):
        self._closed=False
        if not os.path.exists("Data"):
            os.makedirs("Data")
        if not os.path.exists("Log"):
            os.makedirs("Log")
        
        date=time.strftime('%Y-%m-%d')
        ts=time.strftime('%H-%M-%S')
        
        datadir=os.path.join("Data",date)
        if not os.path.exists(datadir):
            os.makedirs(datadir)
        self._dataname=os.path.join(datadir,expname+"_"+date+"_"+ts+".csv")
        
        logdir=os.path.join("Log",date)
        if not os.path.exists(logdir):
            os.makedirs(logdir)
        self._logname=os.path.join(logdir,expname+"_"+date+"_"+ts+".log")
        
        self._datacols=datacols
        self._datawidth=datawidth
        
        self._data=open(self._dataname,'w')
        self._headers_out=False
        
    
    def close(self):
        if not self._closed:
            self._closed=True
            self._data.close()
    def __enter__(self):
        return self
    def __exit__(self,*args):
        self.close()
    
    
    def output_headers(self):        
        headerprep=(lambda h: h.rjust(self._datawidth))\
            if self._datawidth is not None else (lambda h: h)
        self._data.write(",".join([headerprep(d[0])
            for d in self._datacols])+"\n")
        self._headers_out=True
                
    def output_data(self,data):
        assert len(data)==len(self._datacols), "Wrong number of data reported."
        if not self._headers_out:
            self.output_headers()
        data=[f.format(d) for d,(n,f) in zip(data,self._datacols)]
        if self._datawidth is not None:
            data=[d.rjust(self._datawidth) for d in data]
        self._data.write(",".join(data)+"\n")
        
    def output_comment(self,comment):
        if not self._headers_out:
            self.output_headers()
        self._data.write("#"+comment+"\n")
        
    def debug(self,*args,**kwargs):
        print(args)
    def info(self,*args,**kwargs):
        print(args)
    def warning(self,*args,**kwargs):
        print(args)
    def error(self,*args,**kwargs):
        print(args)
    def critical(self,*args,**kwargs):
        print(args)