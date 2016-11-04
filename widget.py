from . events import *
from . geometry import *
from . eventemitter import *

class Widget:
    
    def __init__(self, **kwargs):
        self._pos = (0, 0)
        self._ext = (0, 0)
        self._hovered = False
        # Subscribable events
        self._mouseenter = EventEmitter()
        self._mouseleave = EventEmitter()
        
    @property
    def mouseenter(self): return self._mouseenter

    @property
    def mouseleave(self): return self._mouseleave
    
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
        
    def set_parent(self, parent):
        self._parent = parent
        
    @property
    def root_widget(self):
        return self._parent.root_widget
        
    @property
    def font(self):
        return self.root_widget.default_font
        
    # Dynamic state
    @property
    def hovered(self): return self._hovered
    
    # TODO: make this obsolete by providing a fast RasterizedFont -> FontHandle lookup ?
    @property 
    def fonthandle(self):
        return self.root_widget.default_font_handle
        
    def layout(self):
        raise NotImplementedError("Widget descendents MUST implement the layout method!")
        # TODO: is the above necessarily true ?
        
    def handle_event(self, event, offset):
        #print("Widget.handle_event(): {}".format(event))
        if isinstance(event, MouseMotionEvent):
            #print("event is MouseMotionEvent")
            if Rectangle(self.position + offset, self.extents).contains(event.position):
                if not self.hovered:
                    self._do_mouseenter()
            else:
                if self.hovered:
                    self._do_mouseleave()
    
    def draw(self, canvas, offset):
        raise NotImplementedError("Widget descendents MUST implement the draw() method!")
    
    # FOR DESCENDANTS -----------------------------------------------
    
    def invalidate(self):
        """The invalidate() method triggers a redraw of the widget.
        FIXME: this method should be implemented in an injected aspect [via decorator?]"""        
        
        # This very simple implementation of invalidate() just notifies the container
        assert(self._parent)
        self._parent.child_invalidated(self)
        
    # PRIVATE STUFF -------------------------------------------------
    
    def _do_mouseenter(self):
        self._hovered = True
        self._emit_mouseenter()
        self.invalidate()
        
    def _do_mouseleave(self):
        self._hovered = False
        self._emit_mouseleave()
        self.invalidate()
        
    def _emit_mouseenter(self):
        for subscriber in self._mouseenter: subscriber(self)
        
    def _emit_mouseleave(self): 
        for subscriber in self._mouseleave: subscriber(self)
        