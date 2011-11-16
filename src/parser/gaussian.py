#!/usr/bin/env python

import numpy as np

def onedgaussian(arr, mu = None):
    if mu == None:
        mu = np.mean(arr)
    np.subtract(arr, float(mu), arr)
    arr = np.multiply(arr, arr)
    sig = np.sum(arr)/float(len(arr))
    return mu, sig

def onedgaussian_trigger(arr, mu = None, trigger_sig=10000):
    m,s = onedgaussian(arr, mu)
    return m,s, s>trigger_sig

if __name__ == "__main__":
    import numpy as np
    a = np.arange(100)
    print onedgaussian(a)
