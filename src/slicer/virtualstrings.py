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
    
    def action(self, depth_array):
        # split array into horizontal lines
        for y_idx in range(len(self.spacings)):
            if y_idx in self.zones.keys():
                x_arrs = np.array_split(depth_array[int(self.y_spacing+y_idx*self.y_spacing)], self.x)
                for x_idx in sorted(list(self.zones[y_idx])):
                    array = x_arrs[x_idx]
                    yield ((x_idx, y_idx), array)


"""

RETIRED PoC code


class Horizontal_string(object):
    def __init__(self, config=[4,3], hot_zones=([(x, y) for y in range(3) for x in range(4)]), 
                       func=lambda array: onedgaussian_trigger(np.subtract(2048, array), 
                                                               mu = 2048-np.amin(array), 
                                                               trigger_sig=10000), 
                       res=[640,480]):
        self.cols, self.rows = res # kinect resolution
        self.x, self.y = config
        self.zones = {}
        self.states = {}
        self.func = func
        for zn in hot_zones:
            self.set_hot_zone(zn)
        self.set_horizontal_strings()
    
    def set_hot_zone(self, zone):
        if not self.zones.has_key(zone[1]):
            self.zones[zone[1]] = set()
        self.zones[zone[1]].add(zone[0])
    
    def set_horizontal_strings(self):
        amount = self.y
        if amount > 0 and amount < self.rows:
            self.spacing = int(self.rows / (amount + 1))
            self.x_spacing = (self.cols / self.x)
            self.spacings = [(self.spacing + (self.spacing*i)) for i in range(amount)]
        else:
            print "Bad amount passed to scanner"
            if not self.spacings:
                self.spacings = []
    
    def set_state(self, x, y, data):
        if not self.states.has_key(x):
            self.states[x] = {}
        self.states[x][y] = data
    
    def update_image(self, depth_array):
        img = util.frame_convert.pretty_depth_cv(depth_array)
        # draw strings, deactive and then active strands
        for y in self.spacings:
            cv.Line(img, (0,y), (self.cols, y), 0x00)
        for x, x_blk in self.states.iteritems():
            for y, data in x_blk.iteritems():
                if data[2]:
                    cv.Circle(img, 
                            (int((self.x_spacing/2.0)+self.x_spacing*x), 
                             int(self.spacing + (self.spacing*y))), 50, 0x00)
                else:
                    cv.Circle(img, 
                            (int((self.x_spacing/2.0)+self.x_spacing*x), 
                             int(self.spacing + (self.spacing*y))), 25, 0x33)
        return img
        
    
    def parse(self, depth_array):
        # split array into horizontal lines
        for y_idx in range(len(self.spacings)):
            if y_idx in self.zones.keys():
                x_arrs = np.array_split(depth_array[int(self.spacing+y_idx*self.spacing)], self.x)
                for x_idx in sorted(list(self.zones[y_idx])):
                    array = x_arrs[x_idx]
                    data = self.func(array)
                    self.set_state(x_idx, y_idx, data)
        return self.update_image(depth_array), self.states
    
    
if __name__ == "__main__":
    import freenect, cv
    
    cv.NamedWindow('Depth')
    
    h = Horizontal_string()
    
    while 1:
        img, data = h.parse(freenect.sync_get_depth()[0])
        cv.ShowImage('Depth', img)
        if cv.WaitKey(10) == 27:
            break

"""
