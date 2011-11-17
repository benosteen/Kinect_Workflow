#!/usr/bin/env python

import frame_convert
import cv
import numpy as np

class Grid(object):
    def __init__(self, config={'fn':'binary_circles'}):
        self.config = config
        self.set_fn()
    
    def set_fn(self, fn=None):
        if fn != None:
            if hasattr(self, fn):
                self.config['fn'] = fn
            else:
                print "Couldn't find function '%s' in this class" % fn
                print "Continuing to use %s" % config.get('fn')
        if hasattr(self, self.config.get('fn', 'binary_circles')):
            self.fn = self.__getattribute__(self.config.get('fn', 'binary_circles'))
        
    def binary_circles(self, depth_array, states, local_to_pixel,
                        on_size = 50, on_colour = 0x00,
                        off_size = 25, off_colour = 0x44):
        if self.config.get('threshold'):
            depth_array = np.clip(depth_array, self.config["threshold"].get("min", 200), self.config["threshold"].get("min", 200) + self.config["threshold"].get("range", 300))
        img = frame_convert.pretty_depth_cv(depth_array)
        # draw strings, deactive and then active strands
        for state in states:
            x,y = local_to_pixel(state['label'])
            if state.get('mapped', False):
                cv.Circle(img, (x,y), on_size, on_colour)
            else:
                cv.Circle(img, (x,y), off_size, off_colour)
        return img
    
    def scalar_size_circles(self, depth_array, states, local_to_pixel,
                        state_size_var = "size",
                        colour = 0x00):
        img = frame_convert.pretty_depth_cv(depth_array)
        # draw strings, deactive and then active strands
        for state in states:
            x,y = local_to_pixel(state['label'])
            cv.Circle(img, (x,y), state.get(state_size_var, 0), colour)
        return img
