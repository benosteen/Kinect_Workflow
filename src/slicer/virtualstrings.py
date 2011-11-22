#!/usr/bin/env python

import numpy as np

GRIDX = 4
GRIDY = 3

HORIZONTAL_SLICES_CONFIG = {'x':GRIDX, 
                            'y':GRIDY, 
                            'zones':([(x, y) for y in range(GRIDY) for x in range(GRIDX)]),
                            'res':(640,480)}

class Horizontal_slices(object):
    def __init__(self, config=HORIZONTAL_SLICES_CONFIG):
        self.cols, self.rows = config.get('res', (640,480)) # kinect resolution
        self.config = config
        self.x = config.get('x', GRIDX)
        self.y = config.get('y', GRIDY)
        self.zones = {}
        for zn in config.get('zones'):
            self.set_active_zone(zn)
        self.set_horizontal_strings()
    
    def get_typical_config(self):
        return HORIZONTAL_SLICES_CONFIG

    def local_to_pixel(self, label):
        x, y = label
        return (int((self.x_spacing/2.0)+self.x_spacing*x), int(self.y_spacing + (self.y_spacing*y)))

    def set_active_zone(self, zone):
        # y then x, as this is how the arrays are chunked up
        if not self.zones.has_key(zone[1]):
            self.zones[zone[1]] = set()
        self.zones[zone[1]].add(zone[0])
        
    def set_horizontal_strings(self):
        amount = self.y
        if amount > 0 and amount < self.rows:
            self.y_spacing = int(self.rows / (amount + 1))
            self.x_spacing = (self.cols / self.x)
            self.spacings = [(self.y_spacing + (self.y_spacing*i)) for i in range(amount)]
        else:
            print "Bad amount passed to scanner"
            if not self.spacings:
                self.spacings = []
    
    def fn(self, depth_array, label=None):
        # split array into horizontal lines
        # Ignoring label as this is often an originator of the slices
        for y_idx in range(len(self.spacings)):
            if y_idx in self.zones.keys():
                x_arrs = np.array_split(depth_array[int(self.y_spacing+y_idx*self.y_spacing)], self.x)
                for x_idx in sorted(list(self.zones[y_idx])):
                    array = x_arrs[x_idx]
                    yield ((x_idx, y_idx), array)


