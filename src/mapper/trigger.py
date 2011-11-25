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
    
    def simple_gt(self, label, values):
        # True, False and None for undefined ;)
        if self.varname in values.keys():
            return {'trigger': values[self.varname] > self.config['limit']}

    def simple_lt(self, label, values):
        # True, False and None for undefined ;)
        if self.varname in values.keys():
            return {'trigger': values[self.varname] < self.config['limit']}
        
    def simple_range(self, label, values):
        # True, False and None for undefined ;)
        if self.varname in values.keys():
            return {'trigger': values[self.varname] < self.config['max'] and values[self.varname] > self.config['min']}

    def labelled_range(self, label, values):
        xy = "%s,%s" % label
        f = self.config.get('thresholds', {})
        if xy in f.keys() and self.varname in values.keys():
            min_d, max_d = f[xy]
            return {'trigger': values[self.varname] < max_d and values[self.varname] > min_d}
        else:
            return {'trigger': values[self.varname] < self.config.get('max', 0) and values[self.varname] > self.config.get('min', 0)}
