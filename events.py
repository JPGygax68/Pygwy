from . geometry import Point, Extents

# TODO: more pythonic to define a property that returns the event type, rather than using isinstance() ?

class Event:
    pass
    
class KeyboardEvent:    
    PRESSED = 0
    RELEASED = 1
    
class MouseEvent:
    @property
    def position(self):
        raise NotImplementedException("MouseEvent implementations must implement position property")

class MouseMotionEvent(MouseEvent):
    # TODO
    pass
    
class MouseButtonEvent(MouseEvent):

    @property
    def button(self): raise NotImplementedError("MouseButtonEvent.button")
        
    @property
    def clicks(self): raise NotImplementedError("MouseButtonEvent.clicks")
    
    @property
    def state_is_released(self): raise NotImplementedError("MouseButtonEvent.state_is_released")

    @property
    def state_is_pressed(self): raise NotImplementedError("MouseButtonEvent.state_is_pressed")

class MouseWheelEvent(MouseEvent):

    @property
    def vector(self): raise NotImplementedError("MouseWheelEvent.vector")

class WindowEvent(Event):

    @property
    def size_changed(self): raise NotImplementedError("WindowEvent.size_changed")

    # TODO: map "resized" to "size_change" (what is the difference in SDL2 ?)
    @property
    def resized(self): raise NotImplementedError("WindowEvent.resized")
        
    @property
    def size(self): raise NotImplementedError("WindowEvent.size")
