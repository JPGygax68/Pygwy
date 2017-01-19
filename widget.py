from events import *
from geometry import *
from eventemitter import *

class Widget(Rectangle):
    
    # TODO: define an informative __str__()
    # TODO: "name" property with unique (? within parent or whole hierarchy ?) value and automatic default value 
    
    def __init__(self, font = None, **kwargs):
        super().__init__(**kwargs)
        self._font = font
        self._hovered = False
        # Subscribable events
        self._mouseenter = EventEmitter()
        self._mouseleave = EventEmitter()
        
    @property
    def mouseenter(self): return self._mouseenter

    @property
    def mouseleave(self): return self._mouseleave
    
    @property
    def parent(self): return self._parent
    
    # FIXME: replace with property or simple member field
    def set_parent(self, parent):
        self._parent = parent
        
    @property
    def root_widget(self):
        return self._parent.root_widget
        
    # TODO: the font property actually belongs in an aspect
    
    @property
    def font(self):
        return self._font if self._font else self.root_widget.default_font
        
    @font.setter
    def font(self, fnt):
        self._font = fnt
        
    # Dynamic state
    @property
    def hovered(self): return self._hovered
    
    # TODO: make this obsolete by providing a fast RasterizedFont -> FontHandle lookup ?
    @property 
    def fonthandle(self):
        return self._fonthandle

    def get_bounding_box(self) -> BoundingBox:
        raise NotImplementedError("Widget descendents MUST implement get_bounding_box() query")

    def layout(self):
        raise NotImplementedError("Widget descendents MUST implement the layout method!")
        # TODO: is the above necessarily true ?
        
    def handle_event(self, event, parent_offset):
        #print("Widget.handle_event(): {}".format(event))
        if isinstance(event, MouseMotionEvent):
            pos = event.position - parent_offset
            if self.contains(pos):
                #print("event is MouseMotionEvent, pos: {}, rect: {}, {}".format(pos, self.position, self.extents))
                if not self.hovered:
                    self.do_mouseenter(pos)
            else:
                if self.hovered:
                    self.do_mouseleave(pos)
        return False

    def update_view(self):
        """The update_view() method is where widgets must update their view state to reflect a changed model state."""      
        raise NotImplementedError("Widget descendents MUST implement the update_view() method!")
        
    def init_graphics(self,canvas):
        # FIXME: move this to an aspect class
        #print("Widget.init_graphics()")
        self._fonthandle = canvas.register_font(self.font)

    def draw(self, canvas, offset):
        raise NotImplementedError("Widget descendents MUST implement the draw() method!")
    
    # "PROTECTED" ---------------------------------------------------
    
    def invalidate(self):
        """The invalidate() method triggers a redraw of the widget.
        FIXME: this method should be implemented in an injected aspect [via decorator?]"""        
        
        # This very simple implementation of invalidate() just notifies the container
        assert(self._parent)
        self._parent.child_invalidated(self)
        
    def do_mouseenter(self, pos):
        print("do_mouseenter")
        self._hovered = True
        self._emit_mouseenter(pos)
        self.invalidate()
        
    def do_mouseleave(self, pos):
        print("do_mouseleave")
        self._hovered = False
        self._emit_mouseleave(pos)
        self.invalidate()
        
    # PRIVATE STUFF -------------------------------------------------
    
    def _emit_mouseenter(self, pos):
        for subscriber in self._mouseenter: subscriber(self)
        
    def _emit_mouseleave(self, pos): 
        for subscriber in self._mouseleave: subscriber(self)
        