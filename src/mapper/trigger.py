#!/usr/bin/env python

DEFAULT_CONFIG = {'fn':'simple_gt',
                  'variable':'foo',
                  'limit':10000}

class Trigger(object):
    def __init__(self, config = DEFAULT_CONFIG):
        self.config = config
        self.set_fn()
    
    def set_fn(self, fn=None):
        if fn != None:
            if hasattr(self, fn):
                self.config['fn'] = fn
            else:
                print "Couldn't find function '%s' in this class" % fn
                print "Continuing to use %s" % config.get('fn')
        if hasattr(self, self.config.get('fn', 'mu_as_min')):
            self.fn = self.__getattribute__(self.config.get('fn', 'simple_gt'))
            self.varname = self.config.get("variable")
    
    def simple_gt(self, values):
        # True, False and None for undefined ;)
        if self.varname in values.keys():
            return values[self.varname] > self.config['limit']

    def simple_lt(self, values):
        # True, False and None for undefined ;)
        if self.varname in values.keys():
            return values[self.varname] < self.config['limit']

