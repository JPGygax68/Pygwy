from . geometry import Rectangle, Point

class Draggable(Rectangle):
    
    # TODO: Draggable currently inherits from Rectangle, which is not completely wrong but probably not ideal; the Draggable aspect should make no assumption about the shape that is being dragged.
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hovered = False # FIXME: this is a duplicate if inheriting from Widget -> fix design
        self._rectangle = Rectangle()
        self._dragging = False

    @property
    def rectangle(self):
        """The rectangular zone within which the draggable is allowed to move."""
        return self._rectangle
        
    @rectangle.setter
    def rectangle(self, r):
        self._rectangle = r
        
    @property
    def dragging(self): return self._dragging
    
    @property
    def relative_position(self):
        return self.position - self._rectangle.position
        
    @relative_position.setter
    def relative_position(self, pos):
        self.position = self._rectangle.position + pos
        
    def start_dragging(self, ptrpos):
        """ptrpos:  pointer position when the dragging starts (independent from the position of the Draggable)"""
        
        self._grab_pos = ptrpos
        self._starting_pos = self.position
        self._dragging = True
        print("started dragging")
        
    def drag(self, ptrpos):
        print("starting_pos: {}, ptrpos: {}, grab_pos: {}".format(self._starting_pos, ptrpos, self._grab_pos))
        self._move_to( self._starting_pos + ptrpos - self._grab_pos )
        
    def stop_dragging(self):
        self._dragging = False
        print("stopped dragging")
        
    def move(self, vec):
        self._move_to(self.position + vec)
        
    def _move_to(self, pos):
        pos = pos.constrained(self.rectangle.position, self.rectangle.position + self.rectangle.extents - self.extents)
        print("pos constrained: {}".format(pos))
        self.position = pos
