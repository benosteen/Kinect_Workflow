#!/usr/bin/env python

import numpy as np

class Simple(object):
    def __init__(self, config={'fn':'mean'}):
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
            self.fn = self.__getattribute__(self.config.get('fn', 'mean'))
    
    def mean(self, array):
        m = np.mean(array)
        return {'main':m, 'mean':m}
    def maxi(self, array):
        m = np.max(array)
        return {'main':m, 'maxi':m}
    def mini(self, array):
        m = np.min(array)
        return {'main':m, 'mini':m}

if __name__ == "__main__":
    import numpy as np
    print "Using 'a = np.arange(100)' as the array to work on"
    a = np.arange(100)
    s = Simple()
    print "Default (mean):"
    print s.fn(a)
    print "Maximum (maxi):"
    s.set_fn("maxi")
    print s.fn(a)
    print "Minimum (mini):"
    s.set_fn("mini")
    print s.fn(a)
