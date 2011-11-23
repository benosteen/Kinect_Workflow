#!/usr/bin/env python

import pygame, pygame.midi

pygame.midi.init()

DEFAULT_CONFIG = {'fn':'basic_grid', 'device':0, 'grid_width':5}

class Drums(object):
    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.drumstates = {}
        self.basenote = 35
        self.o = pygame.midi.Output(config.get('device', 0))
        self.set_fn()
    
    def set_fn(self, fn=None):
        if fn != None:
            if hasattr(self, fn):
                self.config['fn'] = fn
            else:
                print "Couldn't find function '%s' in this class" % fn
                print "Continuing to use %s" % config.get('fn')
        if hasattr(self, self.config.get('fn', 'mu_as_min')):
            self.fn = self.__getattribute__(self.config.get('fn', 'basic_grid'))
        
    def basic_grid(self, label, value):
        x,y = label
        drums_no = self.basenote+(x + y*self.config.get('grid_width', 5))
        if drums_no not in self.drumstates.keys():
            self.drumstates[drums_no] = 0

        if self.drumstates[drums_no] and not value.get('trigger', False):
            self.o.note_off(drums_no)
            self.drumstates[drums_no] = 0
        if value.get('trigger', False):
            if self.drumstates[drums_no] != 1:
                self.drumstates[drums_no] = 1
                self.o.note_on(drums_no, 120)
