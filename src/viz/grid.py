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
            if state.get('mapped', {'trigger':False}).get('trigger', False):
                cv.Circle(img, (x,y), self.config.get('on_size', on_size), self.config.get('on_colour', on_colour))
            else:
                cv.Circle(img, (x,y), self.config.get('off_size', off_size), self.config.get('off_colour', off_colour))
        return img
    
    def scalar_size_circles(self, depth_array, states, local_to_pixel,
                        state_size_var = "size",
                        colour = 0x00):
        img = frame_convert.pretty_depth_cv(depth_array)
        # draw strings, deactive and then active strands
        for state in states:
            x,y = local_to_pixel(state['label'])
            cv.Circle(img, (x,y), state.get(self.config.get("state_size_var", state_size_var), 0), self.config.get("colour", colour))
        return img
    
    def square_areas(self, depth_array, states, local_to_pixel,
                      on_colour = 0x00, off_colour = 0x99, on_thickness=2, off_thickness=1):
        if self.config.get('threshold'):
            depth_array = np.clip(depth_array, self.config["threshold"].get("min", 200), self.config["threshold"].get("min", 200) + self.config["threshold"].get("range", 300))
        img = frame_convert.pretty_depth_cv(depth_array)
        for state in states:
            x,y,w,h = local_to_pixel(state['label'])
            if state.get('mapped', {'trigger':False}).get('trigger', False):
                cv.Rectangle(img, (x,y), (x+w, y+h), self.config.get('on_colour', on_colour), self.config.get('on_thickness', on_thickness))
            else:
                cv.Rectangle(img, (x,y), (x+w, y+h), self.config.get('off_colour', off_colour), self.config.get('off_thickness', off_thickness))
        return img
