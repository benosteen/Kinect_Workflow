#!/usr/bin/env python

import numpy as np

GRIDX = 10
GRIDY = 10

DEFAULT_CONFIG = {'x':GRIDX, 
                  'y':GRIDY, 
                  'zones':([(x*2, y*2) for y in range(GRIDY/2) for x in range(GRIDX/2)]),
                  'res':(640,480)}

class Grid(object):
    def __init__(self, config=DEFAULT_CONFIG):
        self.cols, self.rows = config.get('res', (640,480)) # kinect resolution
        self.config = config
        self.x = config.get('x', GRIDX)
        self.y = config.get('y', GRIDY)
        self.zones = {}
        for zn in config.get('zones'):
            self.set_active_zone(zn)
        self.setup_grid()
    
    def setup_grid(self):
        if self.y > 0 and self.y < self.rows and self.x > 0 and self.x < self.cols:
            self.y_spacing = int(self.rows / (self.y))
            self.x_spacing = int(self.cols / self.x)
            # lookups
            self.x_spacings = [(self.x_spacing*i) for i in range(self.x)]
            self.y_spacings = [(self.y_spacing*i) for i in range(self.y)]
        else:
            print "Bad amount passed to scanner"
            if not self.y_spacings:
                self.y_spacings = []
    
    
    def get_typical_config(self):
        return DEFAULT_CONFIG

    def local_to_pixel(self, label):
        x, y = label
        # returns x, y, width, height (upper-left - 0,0)
        if x > (self.x-1):
            x = self.x-1
        elif x<0:
            x = 0
        if y > (self.y-1):
            y = self.y-1
        elif y<0:
            y = 0
        
        return (self.x_spacings[x], self.y_spacings[y], self.x_spacing, self.y_spacing)

    def set_active_zone(self, zone):
        # y then x, as this is how the arrays are chunked up
        if not self.zones.has_key(zone[1]):
            self.zones[zone[1]] = set()
        self.zones[zone[1]].add(zone[0])
        
    def fn(self, depth_array, label=None):
        # split array into horizontal lines
        # Ignoring label as this is often an originator of the slices
        depth_rows = np.array_split(depth_array, self.y)
        for y_idx in range(len(self.y_spacings)):
            if y_idx in self.zones.keys():
                x_arrs = np.array_split(depth_rows[y_idx], self.x, axis=1)
                for x_idx in sorted(list(self.zones[y_idx])):
                    array = x_arrs[x_idx]
                    yield ((x_idx, y_idx), array)


if __name__ == "__main__":
    import numpy as np
    r = np.random.random_integers(0,1024,(480,640))
    g = Grid()
    a = g.fn(r)
    for label, arr in a:
        print label, len(arr), len(arr[0])
        

