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
    def button(self):
        raise NotImplementedError("MouseButtonEvent.button")
        
    @property
    def clicks(self):
        raise NotImplementedError("MouseButtonEvent.clicks")
    
