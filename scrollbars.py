from . container import Container
from . root_widget import RootWidget
from . button import Button
from . geometry import *
from . events import *
from . draggable import Draggable

class Thumb(Draggable):

    def __init__(self):
        super().__init__()
        self.hovered = False
        
    def set_size(self, w, h):
        self.extents = (w, h)
        
    def draw(self, canvas, offset):
        x, y = self.position + offset
        #print("x,y: {}, {}".format(x,y))
        clr = (0.6, 0.6, 0.6, 1) if self.hovered else (0.5, 0.5, 0.5, 1)
        canvas.rectangle(x, y, self.extents[0], self.extents[1], clr)
    
class VerticalScrollbar(Container):
    
    def __init__(self, *args, lengths = (0, 0), **kwargs):
        # TODO: set lengths here, or define extra property ?
        super().__init__(*args, **kwargs)
        self._lengths = lengths
        self._up_btn   = Button(caption = '\uE5C7')
        self._down_btn = Button(caption = '\uE5C5')
        self.add_child(self._up_btn  )
        self.add_child(self._down_btn)
        self._thumb = Thumb()
        self._down_btn.clicked.subscribe(lambda source: print("source: {}".format(source)))

    def layout(self):
        #print("VerticalScrollbar.layout()")
        w, h = self.extents
        self._up_btn.font   = self.root_widget.default_icon_font
        self._down_btn.font = self.root_widget.default_icon_font
        self._down_btn.minimal_size = Extents(w, int(2 * w / 3)) # make arrow buttons square
        self._up_btn.minimal_size   = Extents(w, int(2 * w / 3)) # ditto
        ext_down = self._down_btn.get_optimal_size()
        ext_up   = self._up_btn  .get_optimal_size()
        y1 = ext_down[1]
        self._up_btn.position = Point(0, 0)
        self._up_btn.extents  = (self.extents[0], ext_up[1])
        y2 = self.extents[1] - ext_down[1]
        self._down_btn.position = (0, y2)
        self._down_btn.extents  = (w, ext_down[1])
        ls = y2 - y1 # "slide" length
        lt = min(ls, int(ls * self._lengths[0] / self._lengths[1])) if self._lengths[1] > 0 else ls
        self._thumb.set_size( self.extents[0], lt )
        self._thumb.define_range( (0, y1), (0, y2 - self._thumb.extents[1]) )
        super().layout() # call layout() on children (buttons)
        
    def init_graphics(self, canvas):
        #print("VerticalScrollbar.init_graphics()")
        super().init_graphics(canvas)
        
    def update_view(self):
        self._thumb.relative_position = (0, 0)
        
    def draw(self, canvas, parent_offset):
        #print("VerticalScrollbar.draw()")
        # Draw children
        super().draw(canvas, parent_offset)
        self._thumb.draw(canvas, self.position + parent_offset)

    def handle_event(self, event, parent_offset):
        if isinstance(event, MouseMotionEvent):
            pos = event.position - parent_offset - self.position
            if not self._thumb.hovered and self._thumb.contains(pos):
                self._thumb.hovered = True
                print("hovered!")
                self.invalidate()
            elif self._thumb.hovered and not self._thumb.contains(pos):
                self._thumb.hovered = False
                print("un-hovered!")
                self.invalidate()
            if self._thumb.dragging:
                self._thumb.drag(pos)
                self.invalidate()
        elif isinstance(event, MouseButtonEvent):
            pos = event.position - parent_offset - self.position
            if event.button == 1 and event.state_is_pressed:
                if self._thumb.contains(pos):
                    self._thumb.start_dragging(pos)
            elif event.button == 1 and event.state_is_released:
                if self._thumb.dragging:
                    self._thumb.stop_dragging()
        elif isinstance(event, MouseWheelEvent):
            if self.hovered:
                self._thumb.move( - event.vector )
            return True
                    
        super().handle_event(event, parent_offset)
