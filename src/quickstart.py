from orchestrator import Orchestrator

import cv

import sys


if len(sys.argv) == 2:
    fn = sys.argv[1]
    o = Orchestrator(config_file=fn)
else:
    # Use the default configuration
    fn = "Default configuration"
    o = Orchestrator()

for screen_idx in range(o.number_of_screens()):
    cv.NamedWindow('%s-%s - quickstart' % (fn, screen_idx))

if o.options.get('input', "") != "fake":
    import freenect
    print "Using the kinect as input"
    while 1:
        imgs = o.handle_frame(freenect.sync_get_depth()[0])
        for idx, img in enumerate(imgs):
            cv.ShowImage('%s-%s - quickstart' % (fn, idx), img)
        if cv.WaitKey(10) == 27:
            sys.exit(0)
else:  # fake input
    import numpy as np
    print "Using randomly generated frames as input"
    while 1:
        imgs = o.handle_frame(np.random.random_integers(0,1024,(480,640)))
        for idx, img in enumerate(imgs):
            cv.ShowImage('%s-%s - quickstart' % (fn, idx), img)
        if cv.WaitKey(10) == 0x1b:
            sys.exit(0)
        
