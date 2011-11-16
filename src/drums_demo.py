import freenect, cv

import pygame, pygame.midi

from virtualstrings import Horizontal_string

pygame.midi.init()

o = pygame.midi.Output(0)
 
cv.NamedWindow('Depth')
    
h = Horizontal_string()

drums_start = 36

drums_state = {}

while 1:
    img, data = h.parse(freenect.sync_get_depth()[0])
    for x in data.keys():
        for y in data[x].keys():
            drums_no = drums_start+(x + y*4)
            if drums_no not in drums_state.keys():
                drums_state[drums_no] = False
            if data[x][y][2]:
                if not drums_state[drums_no]:
                    o.note_on(drums_no, 120)
                    drums_state[drums_no] = True
            elif drums_state[drums_no]:
                o.note_off(drums_no)
                drums_state[drums_no] = False
    cv.ShowImage('Depth', img)
    if cv.WaitKey(10) == 27:
        break
