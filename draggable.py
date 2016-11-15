from . geometry import Rectangle, Point

class Draggable(Rectangle):
    
    # TODO: Draggable currently inherits from Rectangle, which is not completely wrong but probably not ideal; the Draggable aspect should make no assumption about the shape that is being dragged.
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.hovered = False # FIXME: this is a duplicate if inheriting from Widget -> fix design
        self._dragging = False

    @property
    def range(self):
        return (self._from_pos, self._to_pos)
        
    @range.setter
    def range(self, points):
        """Defines the range, in both horizontal and vertical directions, that the draggable can move.
        This does NOT take into account the width and height of the rectangle: the restriction applies directly to the origin point."""
        
        self._from_pos = points[0]
        self._to_pos   = points[1]
        self._extents = points[1] - points[0]
    
    @property
    def dragging(self): return self._dragging
    
    @property
    def relative_position(self):
        return self.position - self._from_pos
        
    @relative_position.setter
    def relative_position(self, pos):
        self.position = (self._from_pos[0] + pos[0], self._from_pos[1] + pos[1])
        
    def start_dragging(self, ptrpos):
        """ptrpos:  pointer position when the dragging starts (independent from the position of the Draggable)"""
        
        self._grab_pos = ptrpos
        self._starting_pos = self.position
        self._dragging = True
        print("started dragging")
        
    def drag(self, ptrpos):
        self._move_to( self._starting_pos + ptrpos - self._grab_pos )
        
    def stop_dragging(self):
        self._dragging = False
        print("stopped dragging")
        
    def move(self, vec):
        self._move_to(self.position + vec)
        
    def _move_to(self, pos):
        self.position = Point(max(self._from_pos[0], min(self._to_pos[0], pos[0])), max(self._from_pos[1], min(self._to_pos[1], pos[1])))
