from . geometry import Rectangle

class Draggable(Rectangle):
    
    # TODO: Draggable currently inherits from Rectangle, which is not completely wrong but probably not ideal; the Draggable aspect should make no assumption about the shape that is being dragged.
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dragging = False

    def define_range(self, from_pos, to_pos):
        """Defines the range, in both horizontal and vertical directions, that the draggable can move.
        This does NOT take into account the width and height of the rectangle: the restriction applies directly to the origin point."""
        
        self._from_pos = from_pos
        self._to_pos   = to_pos
        self._extents = (to_pos[0] - from_pos[0], to_pos[1] - from_pos[1])
        
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
        pos = self._starting_pos + ptrpos - self._grab_pos
        self.position = (max(self._from_pos[0], min(self._to_pos[0], pos[0])), max(self._from_pos[1], min(self._to_pos[1], pos[1])))
        print("dragging, ptrpos: {}, position: {}".format(ptrpos, self.position))
        
    def stop_dragging(self):
        self._dragging = False
        print("stopped dragging")