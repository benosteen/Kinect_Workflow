#!/usr/bin/env python

import numpy as np

class Onedgaussian(object):
    def __init__(self, config={'fn':'mu_as_min'}):
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
            self.fn = self.__getattribute__(self.config.get('fn', 'mu_as_min'))
        
    def normal(self, label, arr, mu = None):
        if mu == None:
            mu = np.mean(arr)
        np.subtract(arr, float(mu), arr)
        arr = np.multiply(arr, arr)
        sig = np.sum(arr)/float(len(arr))
        return {'main':sig, 'mu':mu, 'sig':sig}

    def mu_as_min(self, label, arr):
        mu = np.min(arr)
        return self.normal(label, arr, mu)

    def mu_as_max(self, label, arr):
        mu = np.max(arr)
        return self.normal(label, arr, mu)

if __name__ == "__main__":
    import numpy as np
    print "Using 'a = np.arange(100)' as the array to work on"
    a = np.arange(100)
    print "Default 'mu as min':"
    og = Onedgaussian()
    print og.fn(a)
    print "Normal:"
    og.set_fn("normal")
    print og.fn(a)
    print "Mu as Max:"
    og.set_fn("mu_as_max")
    print og.fn(a)
