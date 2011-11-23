#!/usr/bin/env python

DEFAULT_CONFIG = {'fn':'inc',
                  'labels':[(1,2)],
                  'component':'output',
                  'component_index':0,
                  'config_variable': 'scale_index',
                  'amount': 1}

class Controller(object):
    def __init__(self, config={'fn':'inc'}):
        self.config = config
        self.controlstates = {}
        self.set_fn()
    
    def set_fn(self, fn=None):
        if fn != None:
            if hasattr(self, fn):
                self.config['fn'] = fn
            else:
                print "Couldn't find function '%s' in this class" % fn
                print "Continuing to use %s" % config.get('fn')
        if hasattr(self, self.config.get('fn', 'inc')):
            self.fn = self.__getattribute__(self.config.get('fn', 'inc'))
    
    def inc(self, label, value, config = None):
        for control in self.config.get('labels', [(1,2)]):
            if control[0] == label[0] and control[1] == label[1]:
                x,y = label
                control_idx = (x + y*self.config.get('grid_width', 5))
                if control_idx not in self.controlstates.keys():
                    self.controlstates[control_idx] = 0

                if self.controlstates[control_idx] and not value.get('trigger', False):
                    self.controlstates[control_idx] = 0
                if value.get('trigger', False):
                    if self.controlstates[control_idx] != 1:
                        self.controlstates[control_idx] = 1
                        print "Incrementing %s.%s - %s" % (self.config.get('component'), self.config.get('component_index',0), self.config.get('config_variable'))
                        self._inc_config(config)
    
    def _inc_config(self, config):
        if config.has_key(self.config.get('component')) and self.config.get('component_index',0) < len(config[self.config.get('component')]):
            config[self.config.get('component')][self.config.get('component_index',0)]["config"][self.config.get('config_variable')] += self.config.get('amount', 1)
