# -*- coding: utf-8 -*-
"""
Created on Mon Apr  4 20:48:01 2016

@author: Samuel James Bader (samuel.james.bader@gmail.com)
"""
import matplotlib.pyplot as mpl

class DynamicFigure:
    '''http://stackoverflow.com/a/10944967'''
    def __init__(self,*args,**kwargs):
        self._fig=mpl.figure(*args,**kwargs)
        self._elts={}

    def __getattr__(self,attr):
        if(attr=="plot"):
            def hooked(*args,**kwargs):
                dynamic_name=kwargs.get('dynamic_name',None)
                newkwargs={k:kwargs[k] for k in kwargs if k!='dynamic_name'}
                if dynamic_name is not None:
                    if dynamic_name in self._elts:
                        self.update_dynamic_element(dynamic_name,args[0],args[1])
                        return self._elts[dynamic_name]
                    else:
                        output=mpl.plot(*args,**newkwargs)
                        self.add_dynamic_element(output[0],dynamic_name)
                        return output
            return hooked
        else:
            orig_attr = self._fig.__getattribute__(attr)
            return orig_attr
        
    def add_dynamic_element(self,elt,name):
        self._elts[name]=elt
    def update_dynamic_element(self,name,x,y):
        self._elts[name].set_xdata(x)
        self._elts[name].set_ydata(y)
        self.update_plot()
    def rescale_on_update(self,enabled=True):
        self._rescale_on_update=enabled
    def update_plot(self):
        if self.rescale_on_update:
            for ax in self._fig.get_axes():
                ax.relim()
                ax.autoscale_view()
        try:
            self._fig.canvas.draw()
        except Exception as e:
            print("No Fig update: ")
            print(e)