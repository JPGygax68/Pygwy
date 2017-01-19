import sdl2
from events import *
from geometry import Point, Vector

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
    
class MouseWheelWrapper(MouseWrapper, MouseWheelEvent):

    @property
    def vector(self):
        return Vector(self.event.wheel.x, self.event.wheel.y)

class WindowEventWrapper(EventWrapper, WindowEvent):
    
    @property
    def size_changed(self): 
        return self.event.window.event == sdl2.SDL_WINDOWEVENT_SIZE_CHANGED
        
    @property
    def resized(self): 
        return self.event.window.event == sdl2.SDL_WINDOWEVENT_RESIZED

    @property
    def size(self): 
        return Extents(self.event.window.data1, self.event.window.data2)
    
_wrapper_map = {
    sdl2.SDL_KEYDOWN: KeyboardWrapper,
    sdl2.SDL_KEYUP: KeyboardWrapper,
    sdl2.SDL_MOUSEMOTION: MouseMotionWrapper,
    sdl2.SDL_MOUSEBUTTONDOWN: MouseButtonWrapper,
    sdl2.SDL_MOUSEBUTTONUP: MouseButtonWrapper,
    sdl2.SDL_MOUSEWHEEL: MouseWheelWrapper,
    sdl2.SDL_WINDOWEVENT: WindowEventWrapper
}    

def wrap_event(event):
    wrapper = _wrapper_map.get(event.type, EventWrapper)
    #print("wrapper: {}", wrapper)
    return wrapper(event)
    