Description:
------------

A workflow tool for image/data processing, created to allow easy use and iteration of ideas for working
with depth data coming from a kinect camera, using OpenCV and numpy for data manipulation and (at first)
doing MIDI output and visualisations.

Dependancies:
-------------

As this project was written to make my life easier wielding libfreenect, OpenCV, MIDI and Numpy, you can 
expect that having the python wrappers for libfreenect ('freenect'), OpenCV ('cv') and Numpy installed is a 
prerequisite. What you may not know, is that I use pygame's MIDI library for MIDI control and so you will also need
pygame.

tl;dr - freenect, cv, numpy, pygame

Usage:
------

in 'src/', you can run:

    python quickstart.py default.json
    
    This will run the 'default.json' configuration, which uses fake input and is a good way to test that you have pygame and 
    opencv installed correctly before trying to work in the kinect input.

    python quickstart.py kinect.json
    
    This will do exactly the same as above, but use input from the kinect's depth camera. Note, that if you have issues like
    'permission denied on /dev/usb....' the simplest way is to 'sudo chmod a+rw /dev/usb....' and try again.
    
Workflow:
---------

The Orchestrator runs it all - takes in a configuration file and dynamically loads plugins based on this.

Main method is 'handle_frame' - this is passed the raw data you want dealt with and it returns a list of
(OpenCV format) Image objects for display. It handles other forms of output, such as MIDI, via the output plugins
in the configuration.

In detail, this is the workflow it attempts per-frame:

 - 1 to n Slicers - Slice/crop/reflow/scale/etc
    In: depth field (numpy 2d array) and optional 'label' to be preserved if present.
    Out: Yields numpy arrays to process, with local labels/coordinates
    (Slicers are chained together, the next working on the output of the first. Ditto for the other 'levels')
 - 1 to n Parsers - Computes on the individual arrays/segments, and derives value matrix
    In: Arrays with local labels
    Out: Computed value matrix with local labels
 - 1 to n Mappers - Decides what action to take based on value matrix
    In: Value matrix
    Out: True/False or Scalar value associated with local label
 - 1 to n Vizs - Takes output from mapper and original depth field and visualises it
    In: Depth field + mapper output
    Out: OpenCV Image for display
 - 1 to n Outputs - Takes Mapper outputs and turns them into desired outputs (eg MIDI)
    In: Mapper outputs
    Out: Whatever you want

Library paths:
--------------

 - Slicers in 'slicer.XXXX'
 - Parsers in 'parser.XXXX'
 - Mappers in 'mapper.XXXX'
 - Viz in 'viz.XXXX'
 - Output in 'output.XXXX'
 - Configuration presets in 'presets/XXXX'
    
Orchestrator configuration uses Class names to load components, see the default.json file for more information.


