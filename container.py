from . widget import Widget

class Container(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._children = []

    def add_child(self, child):
        self._children.append(child)
        child.set_parent(self)
        
    def init_graphics(self, canvas):
        for child in self._children:
            child.init_graphics(canvas)
            
    def handle_event(self, event, offset):
        """Sends the event to the children, after adding the container's position to the specified offset.
        (This is done so that a widget can more easily compare its own rectangle with the pointer position
        specified in the event, if any.)
        Returns True if one of the children consumed the event, False otherwise."""
        
        #print("Container.handle_event(): event: {}, offset: {}".format(event, offset))
        offset = (offset[0] - self.position[0], offset[1] - self.position[1])
        for child in self._children:
            if child.handle_event(event, offset): return True
        
        return False
        
    def draw(self, canvas, offset):
        for child in self._children:
            child.draw(canvas, (offset[0] + self._pos[0], offset[1] + self._pos[1]))
            
    def child_invalidated(self, child):
        self.invalidate()