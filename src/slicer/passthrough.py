#!/usr/bin/env python

class Passthrough(object):
    def __init__(self, config={}):
        self.config = config # just in case
    
    def local_to_pixel(self, label):
        return (0,0)
    
    def action(self, depth_array):
        yield ((0,0), depth_array)
