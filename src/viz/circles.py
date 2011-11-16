#!/usr/bin/env python

import cv

class Horizontal_slices(object):
    def binary_circles(self, depth_array, states, local_to_pixel,
                        on_size = 50, on_colour = 0x00,
                        off_size = 25, off_colour = 0x44):
        img = util.frame_convert.pretty_depth_cv(depth_array)
        # draw strings, deactive and then active strands
        for state in states:
            x,y = local_to_pixel(state['label'])
            if state.get('triggered', False):
                    cv.Circle(img, (x,y), on_size, on_colour)
                else:
                    cv.Circle(img, (x,y), off_size, off_colour)
        return img
    
    def scalar_size_circles(self, depth_array, states, local_to_pixel,
                        state_size_var = "size",
                        colour = 0x00):
        img = util.frame_convert.pretty_depth_cv(depth_array)
        # draw strings, deactive and then active strands
        for state in states:
            x,y = local_to_pixel(state['label'])
            cv.Circle(img, (x,y), state.get(state_size_var, 0), colour)
        return img
