from . events import *
from . eventemitter import *
from . geometry import Rectangle

class Clickable(Rectangle):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._click = EventEmitter()
        
    @property
    def clicked(self): return self._click
    
    def handle_event(self, event, offset):
        if isinstance(event, MouseButtonEvent):
            if event.button == 1 and event.state_is_released and event.clicks == 1:
                if self.contains( (event.position[0] - offset[0], event.position[1] - offset[1]) ):
                    self._click.emit(self)
        return super().handle_event(event, offset)
