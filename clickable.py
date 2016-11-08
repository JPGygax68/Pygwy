from . events import *
from . eventemitter import *

class Clickable(object):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._click = EventEmitter()
        
    @property
    def clicked(self): return self._click
    
    def handle_event(self, event, offset):
        if isinstance(event, MouseButtonEvent):
            if event.button == 1 and event.clicks == 1:
                self._click.emit(self)
        return super().handle_event(event, offset)
