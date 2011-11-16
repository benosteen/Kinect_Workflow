#!/usr/bin/env python

"""
Orchestrator
============

Handles the process of:
    
    Depth frame -->  Slicer  - - - > 
                        |           |
                     Parser         |
                        |           
                     Mapper  - - - > 
                        |           |
                    Outputs     Visualisation
"""

DEFAULT_CONFIG = {'slicer_module':'virtualstrings',
                  'slicer':'Horizontal_slices',
                  'slicer_config': {'x':5, 
                                    'y':3, 
                                    'zones':([(x, y) for y in range(3) for x in range(5)]),
                                    'res':(640,480)},
                  'parser_module':'gaussian',
                  'parser':'Onedgaussian',
                  'parser_config':{'fn':'mu_as_min'},
                  'mapper_module':'trigger',
                  'mapper':'Trigger',
                  'mapper_config':{'fn':'simple_gt',
                                   'variable':'sig',
                                   'limit':10000},
                  'viz_module':'grid',
                  'viz':'Grid',
                  'viz_config':{'fn':'binary_circles'},
                  'output_module':'midi',
                  'output':'Drums',
                  'output_config':{'fn':'basic_grid',
                                   'device':0}
                  }
                  

class Orchestrator(object):
    def __init__(self, config = DEFAULT_CONFIG, config_file=None):
        if config_file != None:
            self.load_config(config_file)
        else:
            self.config = config
        self.mods = {}
        self.component = {}
        for mod in ('slicer', 'parser', 'mapper', 'viz', 'output'):
            self.load_mod(mod, config.get("%s_module" % mod))
            classname = config.get(mod)
            if classname == None:
                print "'%s' classname for %s not found in " % (classname, mod, config.get[mod])
                raise Exception
            if hasattr(self.mods[mod], classname):
                cls = self.mods[mod].__getattribute__(classname)
                if type(cls) == type:
                    self.component[mod] = self.mods[mod].__getattribute__(classname)(config = config.get("%s_config" % mod))
                    print "%s: Loaded '%s' from '%s'" % (mod.capitalize(), classname, config.get("%s_module" % mod))
                else:
                    print "%s: FAILED '%s' from '%s' - %s is not a class" % (mod.capitalize(), classname, config.get("%s_module" % mod), classname)
            else:
                print "%s: FAILED '%s' from '%s' - class not found in module" % (mod.capitalize(), classname, config.get("%s_module" % mod))
    
    def load_config(self, fn):
        # More error checking required
        fp = open(fn, "r")
        config = json.load(fp)
        fp.close()
        self.config = config
    
    def load_mod(self, mod, name):
        try:
            m = __import__("%s.%s" % (mod, name))
            self.mods[mod] = m.__getattribute__(name)
        except ImportError, e:
            print "Couldn't load %s for %s as configured" % (name, mod)
            raise e

    def handle_frame(self, depth_array):
        outputs = []
        for label, arr in self.component['slicer'].action(depth_array):
            value_matrix = self.component['parser'].fn(arr)
            mapped = self.component['mapper'].fn(value_matrix)
            # output time
            outputs.append({'label':label, 'mapped':mapped})
            self.component['output'].fn(label, mapped)
        return self.component['viz'].fn(depth_array, outputs, self.component['slicer'].local_to_pixel)
        


if __name__ == "__main__":
    o = Orchestrator()
    
    import numpy as np
    import cv
    
    # create fake output
    while 1:
        a = np.random.random_integers(0,255,(480,640))
        img = o.handle_frame(a)
        cv.ShowImage('Drum_demo', img)
        from time import sleep
        if cv.WaitKey(10) == 27:
            exit()
    
