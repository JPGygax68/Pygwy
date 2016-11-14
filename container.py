from . widget import Widget
from . geometry import Point
from . events import *

class Container(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._children = []

    def add_child(self, child):
        self._children.append(child)
        child.set_parent(self)
        
    def layout(self):
        for child in self._children:
            child.layout()
            
    def update_view(self):
        for child in self._children:
            child.update_view()
            
    def init_graphics(self, canvas):
        super().init_graphics(canvas)
        for child in self._children:
            child.init_graphics(canvas)
            
    def handle_event(self, event, parent_offset):
        """Sends the event to the children, after adding the container's position to the specified parent offset.
        (This is done so that a widget can more easily compare its own rectangle with the pointer position
        specified in the event, if any.)
        Returns True if one of the children consumed the event, False otherwise."""
        
        offset = parent_offset + self.position
        for child in self._children:        
            if isinstance(event, MouseWheelEvent) and self.hovered:
                if child.handle_event(event, offset): return True
            # TODO: more special handling; mouse capture etc.
            else:
                if child.handle_event(event, offset): return True
        
        return super().handle_event(event, parent_offset)
        
    def draw(self, canvas, offset):
        offset = offset + self.position
        for child in self._children:
            child.draw(canvas, offset)
            
    def child_invalidated(self, child):
        self.invalidate()