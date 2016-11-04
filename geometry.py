import collections

Point   = collections.namedtuple('Point', 'x y')
Extents = collections.namedtuple('Extents', 'w h')

class Rectangle:
    
    def __init__(self, origin, extents):
        self.origin = origin
        self.extents  = extents
        
    def contains(self, point):
        return (point[0] >= self.origin[0] and point[0] < self.origin[0] + self.extents[0]
            and point[1] >= self.origin[1] and point[1] < self.origin[1] + self.extents[1])