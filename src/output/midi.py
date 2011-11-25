#!/usr/bin/env python

import pygame, pygame.midi

pygame.midi.init()

DEFAULT_CONFIG = {'fn':'basic_grid', 'device':0, 'grid_width':5}

SCALES = {'CMAJOR': [0,2,4,5,7,9,11],
          'BLUES': [0,3,5,6,7,10,11],
          'MAJORPENT': [0,2,4,7,11],
          'MINORPENT': [0,3,5,7,10],
          'JAZZY': [0,2,4,6,8,10],
          'INSEN': [0,1,5,7,10],
          'HIRAJOSHI': [0,1,5,7,9],
          'THIRDS': [0,4,2,5,4,7,5,9,7,11,13,12],
          'CHROMATIC': [0,1,2,3,4,5,6,7,8,9,10,11]
          }

SCALESLIST = sorted(SCALES.keys())   # In case we want to iterate over them

class Scales(object):
    def __init__(self, config=DEFAULT_CONFIG):
        self.config = config
        self.keystates = {}
        self.basenote = 0
        self.octave = 12
        self.o = pygame.midi.Output(config.get('device', 0))
        self.set_fn()
    
    def set_fn(self, fn=None):
        if fn != None:
            if hasattr(self, fn):
                self.config['fn'] = fn
            else:
                print "Couldn't find function '%s' in this class" % fn
                print "Continuing to use %s" % config.get('fn')
        if hasattr(self, self.config.get('fn', 'basic_grid')):
            self.fn = self.__getattribute__(self.config.get('fn', 'basic_grid'))
        
    def basic_grid(self, label, value, config=None):
        x,y = label
        if self.config.get("y") != None and y not in self.config.get("y"):
            return
        note_idx = self.basenote+(x + y*self.config.get('grid_width', 5))
        scale =  SCALES.get(self.config.get('scale', 'CMAJOR'), SCALES['CMAJOR'])
        note = 12 * (note_idx / len(scale)) + (scale[note_idx % len(scale)]) + self.config.get('transpose', 0)
        if self.config.get("wrap"):
            note = note % self.config["wrap"]
        if note_idx not in self.keystates.keys():
            self.keystates[note_idx] = 0

        if self.keystates[note_idx] and not value.get('trigger', False):
            self.o.note_off(note)
            self.keystates[note_idx] = 0
        if value.get('trigger', False):
            if self.keystates[note_idx] != 1:
                self.keystates[note_idx] = 1
                self.o.note_on(note, 120)
                
    def basic_grid_multiple_scales(self, label, value, config=None):
        x,y = label
        if self.config.get("y") != None and y not in self.config.get("y"):
            return
        note_idx = self.basenote+(x + y*self.config.get('grid_width', 5))
        self.config['scale_index'] = self.config.get('scale_index', 0) % len(SCALESLIST)
        scale =  SCALES.get(SCALESLIST[self.config.get('scale_index', 0) ] )
        note = 12 * (note_idx / len(scale)) + (scale[note_idx % len(scale)]) + self.config.get('transpose', 0)
        if self.config.get("wrap"):
            note = note % self.config["wrap"]
        if note_idx not in self.keystates.keys():
            self.keystates[note_idx] = 0

        if self.keystates[note_idx] and not value.get('trigger', False):
            self.o.note_off(note)
            self.keystates[note_idx] = 0
        if value.get('trigger', False):
            if self.keystates[note_idx] != 1:
                self.keystates[note_idx] = 1
                self.o.note_on(note, 120)
                
    def basic_grid_custom_scale(self, label, value, config=None):
        x,y = label
        if self.config.get("y") != None and y not in self.config.get("y"):
            return
        note_idx = self.basenote+(x + y*self.config.get('grid_width', 5))
        scale =  self.config.get('scalenotes', SCALES['CMAJOR'])
        note = 12 * (note_idx / len(scale)) + (scale[note_idx % len(scale)]) + self.config.get('transpose', 0)
        if self.config.get("wrap"):
            note = note % self.config["wrap"]
        if note_idx not in self.keystates.keys():
            self.keystates[note_idx] = 0

        if self.keystates[note_idx] and not value.get('trigger', False):
            self.o.note_off(note)
            self.keystates[note_idx] = 0
        if value.get('trigger', False):
            if self.keystates[note_idx] != 1:
                self.keystates[note_idx] = 1
                self.o.note_on(note, 120)


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
        if hasattr(self, self.config.get('fn', 'basic_grid')):
            self.fn = self.__getattribute__(self.config.get('fn', 'basic_grid'))
        
    def basic_grid(self, label, value, config=None):
        x,y = label
        if self.config.get("y") != None and y not in self.config.get("y"):
            return
        drums_no = int(self.config.get("drums_start", self.basenote)+(x*self.config.get("step", 1) + y*self.config.get('grid_width', 5)))
        if self.config.get("wrap"):
            drums_no = drums_no % self.config["wrap"]
        if drums_no not in self.drumstates.keys():
            self.drumstates[drums_no] = 0

        if self.drumstates[drums_no] and not value.get('trigger', False):
            self.o.note_off(drums_no)
            self.drumstates[drums_no] = 0
        if value.get('trigger', False):
            if self.drumstates[drums_no] != 1:
                self.drumstates[drums_no] = 1
                self.o.note_on(drums_no, 120)

