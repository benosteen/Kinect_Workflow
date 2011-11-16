from orchestrator import Orchestrator

# Use the default configuration
o = Orchestrator()
    
import freenect, cv
    
cv.NamedWindow('Drum_demo')
    
while 1:
    img = o.handle_frame(freenect.sync_get_depth()[0])
    cv.ShowImage('Drum_demo', img)
    if cv.WaitKey(10) == 27:
        break
