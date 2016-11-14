from . geometry import Rectangle, Extents

class UIElement(Rectangle):

    @property
    def minimal_size(self):
        return Extents(0, 0)

class Sizeable(UIElement):

    @property
    def minimal_size(self):
        return self._min_size
        
    @minimal_size.setter
    def minimal_size(self, size):
        self._min_size = size