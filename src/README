Workflow:
---------

Get Depth field from libfreenect - 'd'

Pass to Orchestrator - components:

 - Slicer - Slice/crop/reflow/scale/etc
    In: depth field (numpy array of rows)
    Out: Yields arrays to process, with local labels/coordinates
 - Parser - Computes on the individual arrays/segments, and derives value matrix
    In: Arrays with local labels
    Out: Computed value matrix with local labels
 - Mapper - Decides what action to take based on value matrix
    In: Value matrix
    Out: True/False or Scalar value associated with local label
 - Viz - Takes output from mapper and original depth field and visualises it
    In: Depth field + mapper output
    Out: OpenCV Image for display
 - Output - Takes Mapper outputs and turns them into desired outputs (eg MIDI)
    In: Mapper outputs
    Out: Whatever you want

Library paths:
    Slicers in 'slicer.XXXX'
    Parsers in 'parser.XXXX'
    Mappers in 'mapper.XXXX'
    Viz in 'viz.XXXX'
    Output in 'output.XXXX'
    
Orchestrator configuration uses Class names to load components
