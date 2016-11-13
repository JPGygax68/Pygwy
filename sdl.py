import sdl2
from . events import *
from . geometry import Point

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
        return Point(self.event.motion.x, self.event.motion.y)

class MouseMotionWrapper(MouseWrapper, MouseMotionEvent):
    pass
    
class MouseButtonWrapper(MouseWrapper, MouseButtonEvent):

    #def __init__(self, event):
    #    super().__init__(event)
    #    print("MouseButtonWrapper")
        
    @property
    def button(self): return self.event.button.button
        
    @property
    def clicks(self): return self.event.button.clicks
    
    @property
    def state_is_released(self): return self.event.button.state == sdl2.SDL_RELEASED
    
    @property
    def state_is_pressed(self): return self.event.button.state == sdl2.SDL_PRESSED
    
_wrapper_map = {
    sdl2.SDL_KEYDOWN: KeyboardWrapper,
    sdl2.SDL_KEYUP: KeyboardWrapper,
    sdl2.SDL_MOUSEMOTION: MouseMotionWrapper,
    sdl2.SDL_MOUSEBUTTONDOWN: MouseButtonWrapper,
    sdl2.SDL_MOUSEBUTTONUP: MouseButtonWrapper,
}    

def wrap_event(event):
    wrapper = _wrapper_map.get(event.type, EventWrapper)
    #print("wrapper: {}", wrapper)
    return wrapper(event)
    