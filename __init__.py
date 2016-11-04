import os

from . fontrast import FontRasterizer
from . canvas import Canvas
from . container import Container
from . label import Label
from . button import Button

# FIXME: use resources
thisdir = os.path.dirname(os.path.realpath(__file__))

class RootWidget(Container):

    global thisdir
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.font_rasterizer = FontRasterizer()
        # FIXME: use resources
        self._dflt_rastfont = self.font_rasterizer.rasterize_font(os.path.join(thisdir, "fonts/LiberationSans-Regular.ttf"), 18)
        self._canvas = Canvas()
        self._must_redraw = False
        
    def init_graphics(self):
        """Initialize the canvas and obtain graphics resources."""
        
        self._canvas.init()
        self.dflt_fonthandle = self._canvas.register_font(self._dflt_rastfont)
        
    @property
    def root_widget(self):
        return self
        
    @property
    def default_font(self):
        """A font that can be used as a default by contained widgets."""
        
        return self._dflt_rastfont

    @property
    def default_font_handle(self):
        """A font handle (instance of canvas.FontHandle) that widgets can use as their default font.
        Note that this font handle is only available and valid after init_graphics() has been 
        called."""
        
        return self.dflt_fonthandle

    @property
    def must_redraw(self): 
        """This dynamic, read-only property informs user code whether or not the widget hierarchy
        needs to be redrawn.
        FIXME: this belongs into an aspect; not all updating mechanisms use this property."""
        
        return self._must_redraw
    
    def set_extents(self, w, *h):
        """Set the size of the viewport the root widget will be responsible for,
        either as two integers or a tuple of two integers."""
        self._extents = (w, *h) if h else w
        self._canvas.set_extents(self._extents)
        #print("Extents: {}".format(self._extents))

    def handle_event(self, event):
        """Inject the specified event into the widget hierarchy. Returns True if the event was
        consumed, False otherwise."""        
        #print("RootWidget.handle_event(): {}".format(event))
        return super().handle_event(event, (0, 0))
        
    def render(self):
        with self._canvas:
            self.draw(self._canvas, (0, 0))
        # FIXME: the following belongs into an aspect
        self._must_redraw = False
            
    def invalidate(self):
        self._must_redraw = True
