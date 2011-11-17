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

DEFAULT_CONFIG = {'orchestrator':{'fliplr':True, "input":"fake"},
                  'slicer': [{'module':'virtualstrings',
                             'cls':'Horizontal_slices',
                             'config': {'x':5, 
                                        'y':3, 
                                        'zones':([(x, y) for y in range(3) for x in range(5)]),
                                        'res':(640,480)}
                                }
                            ],
                  'parser': [{'module':'gaussian',
                             'cls':'Onedgaussian',
                             'config':{'fn':'mu_as_min'}
                             }],
                  'mapper': [{'module':'trigger',
                             'cls':'Trigger',
                             'config':{'fn':'simple_gt',
                                       'variable':'sig',
                                       'limit':10000}
                            }],
                  'viz': [{'module':'grid',
                           'cls':'Grid',
                           'config':{'fn':'binary_circles'}
                           }],
                  'output': [{'module':'midi',
                              'cls':'Drums',
                              'config':{'fn':'basic_grid',
                                        'device':0}
                            }]
                  }


import numpy as np                  

class Orchestrator(object):
    def __init__(self, config = DEFAULT_CONFIG, config_file=None):
        if config_file != None:
            config = self.load_config(config_file)
            
        self.config = config
        self.options = config.get('orchestrator', {})        
        self.mods = {}
        self.component = {}
        for mod in ('slicer', 'parser', 'mapper', 'viz', 'output'):
            for idx, item in enumerate(config.get(mod, [])):
                self.load_mod(mod, item.get("module"))
                classname = item.get('cls')
                if classname == None:
                    print "'%s' classname ('cls') for a %s not found in config %s" % (classname, mod, item)
                    raise Exception
                if hasattr(self.mods[mod][idx], classname):
                    cls = self.mods[mod][idx].__getattribute__(classname)
                    if type(cls) == type:
                        if not self.component.get(mod):
                            self.component[mod] = []
                        self.component[mod].append(self.mods[mod][idx].__getattribute__(classname)(config = item.get("config", {})))
                        print "%s: At pos. %s - Loaded '%s/%s' from '%s'" % (mod.capitalize(), idx, classname, item["config"].get('fn', 'fn'), item.get("module"))
                    else:
                        print "%s: FAILED '%s' from '%s' - %s is not a class" % (mod.capitalize(), classname, item.get("module"), classname)
                else:
                    print "%s: FAILED '%s' from '%s' - class not found in module" % (mod.capitalize(), classname, item.get("module"))
    
    def load_config(self, fn):
        # More error checking required
        try:
            import json
        except ImportError:
            import simplejson as json
        fp = open(fn, "r")
        config = json.load(fp)
        fp.close()
        return config
    
    def load_mod(self, mod, name):
        try:
            m = __import__("%s.%s" % (mod, name))
            if not isinstance(self.mods.get(mod, 0), list):
                self.mods[mod] = []
            self.mods[mod].append(m.__getattribute__(name))
        except ImportError, e:
            print "Couldn't load %s for %s as configured" % (name, mod)
            raise e

    def handle_frame(self, depth_array):
        outputs = []
        if self.options.get('fliplr'):
            depth_array = np.fliplr(depth_array)
        for label, out_arr in self.component['slicer'][0].fn(depth_array):
            arr = out_arr     # hard copy or copy ref as here?
            # extra slicer actions (clip, crop, threshold, etc)
            if len(self.component['slicer']) > 1:
                for x in self.component['slicer'][1:]:
                    label, arr = x.fn(arr, label=label)
            # parser steps
            for x in self.component['parser']:
                arr = x.fn(arr)
            # mapper steps
            for x in self.component['mapper']:
                arr = x.fn(arr)
            # output time
            outputs.append({'label':label, 'mapped':arr})
            for x in self.component['output']:
                x.fn(label, arr)
        return [y.fn(depth_array, outputs, self.component['slicer'][0].local_to_pixel) for y in self.component['viz']]  # first slicer labels it, so has responsibility
        
    def save_config(self, filename):
        try:
            import json
        except ImportError:
            import simplejson as json
        fp = open(filename, "w")
        json.dump(self.config, fp, indent=1)
        fp.close()
    
    def number_of_screens(self):
        return len(self.component['viz'])

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 2:
        o = Orchestrator(config_file=sys.argv[1])
    else:
        o = Orchestrator(config_file="default.json")
    import cv
    
    # create fake output
    while 1:
        a = np.random.random_integers(0,1024,(480,640))
        imgs = o.handle_frame(a)
        assert len(imgs) == 1
        cv.ShowImage('Drum_demo', imgs[0])
        from time import sleep
        if cv.WaitKey(10) == 27:
            exit()
    
