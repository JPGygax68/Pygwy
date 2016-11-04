import sdl2
from . events import *

class EventWrapper(Event):
    def __init__(self, event):
        self.event = event
        
class KeyboardWrapper(EventWrapper, KeyboardEvent):
        
    @property
    def state():
        return UP if self.event.type == sdl2.SDL_KEYDOWN else DOWN

class MouseWrapper(EventWrapper, MouseEvent):
    
    @property
    def position(self):
        return (self.event.motion.x, self.event.motion.y)

class MouseMotionWrapper(MouseWrapper, MouseMotionEvent):
    pass
    
class MouseButtonWrapper(MouseWrapper, MouseButtonEvent):
    pass
    
_wrapper_map = {
    sdl2.SDL_KEYDOWN: KeyboardWrapper,
    sdl2.SDL_KEYUP: KeyboardWrapper,
    sdl2.SDL_MOUSEMOTION: MouseMotionWrapper,
}    

def wrap_event(event):
    return _wrapper_map.get(event.type, EventWrapper)(event)
    