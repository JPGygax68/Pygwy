from geometry import Rectangle, Extents


# EXPERIMENTAL, DO NOT USE FOR THE MOMENT!
class Sizeable(UIElement):
    """A Sizeable is a UI element that can have size constraints set on it. At the time of writing, the only constraint
    is the minimal_size property.
    EXPERIMENTAL: it is not certain whether and if so, where this is going to be useful."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._min_size = Extents(0, 0)

    @property
    def minimal_size(self):
        return self._min_size

    @minimal_size.setter
    def minimal_size(self, size):
        self._min_size = size
