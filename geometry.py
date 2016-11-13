import collections

# TODO: make Point and Extents into real classes, with convenience methods and operators, and use them in Rectangle
#Point   = collections.namedtuple('Point', 'x y')
#Extents = collections.namedtuple('Extents', 'w h')

class Point(collections.namedtuple('_Point', 'x y')):

    def __add__(self, delta):
        return Point(self[0] + delta[0], self[1] + delta[1])
        
    def __sub__(self, delta):
        return Point(self[0] - delta[0], self[1] - delta[1])
    
class Extents(collections.namedtuple('_Extents', 'w h')):
    pass
    
class Rectangle:
    
    def __init__(self, origin = Point(0, 0), extents = Extents(0, 0), **kwargs):
        super().__init__(**kwargs)
        self._pos = origin
        self._ext  = extents
        
    @property
    def position(self):
        return self._pos
        
    @position.setter
    def position(self, x, *y):
        self._pos = Point(x, *y) if y else Point(x[0], x[1])

    @property
    def extents(self):
        return self._ext
        
    @extents.setter
    def extents(self, w, *h):
        self._ext = Extents(w, *h) if h else Extents(w[0], w[1])
        
    def contains(self, point):
        return (point[0] >= self._pos[0] and point[0] < self._pos[0] + self._ext[0]
            and point[1] >= self._pos[1] and point[1] < self._pos[1] + self._ext[1])