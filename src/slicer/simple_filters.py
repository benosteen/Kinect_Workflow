#!/usr/bin/env python

import numpy as np

class Filter(object):
    def __init__(self, config={'fn':'threshold',
                               'min':100,
                               'range':200}):
        self.config = config
        self.states = {}
        self.set_fn()
    
    def set_fn(self, fn=None):
        if fn != None:
            if hasattr(self, fn):
                self.config['fn'] = fn
            else:
                print "Couldn't find function '%s' in this class" % fn
                print "Continuing to use %s" % config.get('fn')
        if hasattr(self, self.config.get('fn', 'binary_circles')):
            self.fn = self.__getattribute__(self.config.get('fn', 'threshold'))
    
    def threshold(self, array, label=None):
        return (label, np.clip(array, self.config.get('min', 100), self.config.get('min', 100) + self.config.get('range', 200)))
    
    def background_remove(self, array, label=None):
        if label == None:
            print "Can't perform a background filter, without knowledge of where the array comes from"
            return (label, array)
        if not self.states.has_key(label):
            self.states[label] = []
            self.states[label].append(array)
            return (label, array) # can't do anything without history
        
        self.states[label].append(array)
        
        
        if len(self.states[label]) > self.config.get('limit', 5):
            _ = self.states[label].pop(0)
        # Average seen frames and subtract them from array 
        
