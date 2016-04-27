"""
.. module:: experiment
   :synopsis: The overall experiment object

.. moduleauthor:: Samuel James Bader <samuel.james.bader@gmail.com>


"""

from empyrical.dataflow.logger import LogManager,FakeLogManager
from threading import Thread
import time

class Experiment:
    '''Manages the instruments and dataflow for an experiment
    
    .. note::
        use like::
            with Experiment(name, req_inst, datacols) as exp
                pass
    '''
    
    def __init__(self,experiment_name,required_instruments,datacols):
        '''Initialize all the instruments and the log manager'''
        self._closed=False
        self._inst_dict={}
        self._threads=[]
        try:
            self._lm=LogManager(experiment_name,datacols)
            for inst_name,inst_man,inst_type,inst_id in required_instruments:
                import importlib
                modulename="empyrical.instruments."+inst_man.lower()
                mod=importlib.import_module(modulename)
                self._inst_dict[inst_name]=(getattr(mod,inst_type))(inst_id)
        except Exception as e:
            print(e)
            self.close()

    def close(self):
        '''Closes all instruments and the logger'''
        if not self._closed:
            self._closed=True
            for t,ef in self._threads:
                if t.is_alive():
                    ef.should_exit=True
                    try: t.join(5)
                    except: pass
            for inst in self._inst_dict.values():
                try: inst.close()
                except: pass
            self._lm.close()
    
    def __enter__(self):
        return self
        
    def __exit__(self,*args):
        def close_when_done():
            while(1):
                if self._closed:
                    return
                self._threads=[(t,ef) for t,ef in self._threads if t.is_alive()]
                if not(len(self._threads)):
                    break
                time.sleep(1)
            self.close()
        Thread(target=close_when_done).start()
    
    def run(self,procedure,*args,blocking=False,**kwargs):
        
        ef=ExitFlag()
        kwargs.update(self._inst_dict)
        kwargs.update({'logger':self._lm,'exit_flag':ef})
        if not blocking:
            thread=Thread(target=procedure,args=args,kwargs=kwargs)
            self._threads+=[[thread,ef]]
            thread.start()
            return [
                ef,
                self._lm.get_dataname(),
                self._lm.get_logname()
            ]
        else:
            return [
                procedure(*args,**kwargs),
                self._lm.get_dataname(),
                self._lm.get_logname()
            ]
        
class ExitFlag:
    def __init__(self):
        self.should_exit=False
    
                    
                
                
            
            