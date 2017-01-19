from events import *
from eventemitter import *
from geometry import Rectangle

class CustomClickable(Rectangle): # TODO: use even more generic geometry class ?

    #def __init__(self, **kwargs):
    #    super().__init__(**kwargs)
        
    def handle_event(self, event, offset):
        if isinstance(event, MouseButtonEvent):
            if event.button == 1 and event.state_is_released: # and event.clicks == 1:
                if self.contains(event.position - offset):
                    self.do_clicked()
        return super().handle_event(event, offset)
        
    def do_clicked(self):
        raise NotImplementedError("CustomClickable.do_clicked()")

class ClickedEmitter(CustomClickable):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._click = EventEmitter()
        
    @property
    def clicked(self): return self._click
   
    def do_clicked(self):
        self._click.emit(self)
