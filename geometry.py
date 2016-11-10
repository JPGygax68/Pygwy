import collections

# TODO: make Point and Extents into real classes, with convenience methods and operators, and use them in Rectangle
Point   = collections.namedtuple('Point', 'x y')
Extents = collections.namedtuple('Extents', 'w h')

class Rectangle:
    
    def __init__(self, origin = (0, 0), extents = (0, 0), **kwargs):
        super().__init__(**kwargs)
        self._pos = origin
        self._ext  = extents
        
    @property
    def position(self):
        return self._pos
        
    @position.setter
    def position(self, x, *y):
        self._pos = (x, *y) if y else x

    @property
    def extents(self):
        return self._ext
        
    @extents.setter
    def extents(self, w, *h):
        self._ext = (w, *h) if h else w
        
    def contains(self, point):
        return (point[0] >= self._pos[0] and point[0] < self._pos[0] + self._ext[0]
            and point[1] >= self._pos[1] and point[1] < self._pos[1] + self._ext[1])