from . geometry import Rectangle

class Draggable(Rectangle):
    
    # TODO: Draggable currently inherits from Rectangle, which is not completely wrong but 
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._dragging = False

    def define_range(self, from_pos, to_pos):
        self._from_pos = from_pos
        self._to_pos   = to_pos
        self._extents = (to_pos[0] - from_pos[0], to_pos[1] - from_pos[1])
        
    @property
    def dragging(self): return self._dragging
    
    @property
    def relative_position(self):
        return (self.position[0] - self._from_pos[0], self.position[1] - self._from_pos[1])
        
    @relative_position.setter
    def relative_position(self, pos):
        self.position = (self._from_pos[0] + pos[0], self._from_pos[1] + pos[1])
        
    def start_dragging(self, refpos):
        self._starting_refpos = refpos
        self._dragging = True
        print("started dragging")
        
    def drag(self, refpos):
        #self._current_refpos = refpos
        pos = (self._from_pos[0] + refpos[0] - self._starting_refpos[0], self._from_pos[1] + refpos[1] - self._starting_refpos[1])
        self.position = (max(self._from_pos[0], min(self._to_pos[0], pos[0])), max(self._from_pos[1], min(self._to_pos[1], pos[1])))
        print("dragging, refpos: {}, position: {}".format(refpos, self.position))
        
    def stop_dragging(self):
        self._dragging = False
        print("stopped dragging")