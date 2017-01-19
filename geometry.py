import collections

# TODO: make Point and Extents into real classes, with convenience methods and operators, and use them in Rectangle
#Point   = collections.namedtuple('Point', 'x y')
#Extents = collections.namedtuple('Extents', 'w h')

class Point(collections.namedtuple('_Point', 'x y')):

    def __add__(self, delta):
        return Point(self[0] + delta[0], self[1] + delta[1])
        
    def __sub__(self, delta):
        return Point(self[0] - delta[0], self[1] - delta[1])
    
    def __neg__(self):
        return Point( - self[0], - self[1] )
        
    def constrained(self, start, end):
        return Point( max(min(self[0], end[0]), start[0]), max(min(self[1], end[1]), start[1]) )
        
    #def max(self, other):
    #    return Point( max(self[0], other[0]), max(self[1], other[1]) )
        
    def clip_y(self, y_min, y_max):
        y = max(self[1], y_min)
        y = min(y, y_max)
        self = Point(self[0], y)
   

class Vector(Point):
    pass

class Extents(object):

    def __init__(self, w=None, h=None):
        if w is None:
            self.w = 0
            self.h = 0
        else:
            if h is None:
                self.w, self.h = w
            else:
                self.w = w
                self.h = h

    def __or__(self, other):
        """Arithmetic OR operator: returns the smallests extents that can fit either of the operands."""
        
        return Extents( max(self.x, other.x), max(self.y, other.y) )
        
    def __and__(self, other):
        """Arithmetic AND operator: returns the largets extents that will fit into either of the operands."""

        return Extents( min(self.x, other.x), min(self.y, other.y) )
    
    #def min(self, other):
    #    return Extents( min(self[0], other[0]), min(self[1], other[1]) )
        
    #def max(self, other):
    #    return Extents( max(self[0], other[0]), max(self[1], other[1]) )
    
class Rectangle(object):
    
    def __init__(self, origin = Point(0, 0), extents = Extents(0, 0), **kwargs):
        super().__init__(**kwargs)
        self._pos = origin
        self._ext = extents
        
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
        if type(w) is tuple:
            self._ext.w = w[0]
            self._ext.h = w[1]
        elif type(w) is Extents:
            assert not h
            self._ext = w
        else:
            assert h
            self._ext = Extents(w, *h)
            
    @property
    def width(self):
        return self.extents.w
        
    @property
    def height(self):
        return self.extents.h
        
    def contains(self, point):
        return (point.x >= self._pos.x and point.x < self._pos.x + self._ext.w
            and point.y >= self._pos.y and point.y < self._pos.y + self._ext.h)
            

class BoundingBox(Extents):
    """A BoundingBox is an extension of the Extents class. It splits the height into two components "ascender" and
    "descender", so that the box can be correctly positioned on a typographical baseline.
    """

    def __init__(self, width, ascender_or_height, descender=None):
        super().__init__()
        self.w = width
        if descender is None:
            self.h = ascender_or_height
            self.descender = self.h // 2
        else:
            self.h = ascender_or_height + descender
            self.descender = self.h - ascender_or_height

    @property
    def ascender(self):
        return self.h - self.descender


