from container import Container
from root_widget import RootWidget
from button import CustomButton
from geometry import *
from events import *
from draggable import Draggable
from eventemitter import *

class Thumb(Draggable):

    def __init__(self):
        super().__init__()
        
    def set_size(self, w, h):
        self.extents = (w, h)
        
    def draw(self, canvas, offset):
        x, y = self.position + offset
        #print("x,y: {}, {}".format(x,y))
        clr = (0.6, 0.6, 0.6, 1) if self.hovered else (0.5, 0.5, 0.5, 1)
        canvas.rectangle(x, y, self.extents[0], self.extents[1], clr)
    
class ScrollUpButton(CustomButton):
    def __init__(self, *args, **kwargs):
        super().__init__(caption='\uE5C7', *args, **kwargs)
    def do_clicked(self):
        self.parent.line_up()
        
class ScrollDownButton(CustomButton):
    def __init__(self, *args, **kwargs):
        super().__init__(caption='\uE5C5', *args, **kwargs)
    def do_clicked(self):
        self.parent.line_down()
        
class VerticalScrollbar(Container):
    
    def __init__(self, *args, lengths = (0, 0), **kwargs):
        # TODO: set lengths here, or define extra property ?
        super().__init__(*args, **kwargs)
        self._lengths = lengths
        self._up_btn   = ScrollUpButton()
        self._down_btn = ScrollDownButton()
        self.add_child(self._up_btn  )
        self.add_child(self._down_btn)
        self._thumb = Thumb()
        #self._down_btn.clicked.subscribe(lambda source: print("source: {}".format(source)))
        self._position_changed = EventEmitter()

    @property
    def position_changed(self): return self._position_changed
    
    def layout(self):
        #print("VerticalScrollbar.layout()")
        w, h = self.extents
        self._up_btn.font   = self.root_widget.default_icon_font
        self._down_btn.font = self.root_widget.default_icon_font
        self._down_btn.minimal_size = Extents(w, int(2 * w / 3))
        self._up_btn.minimal_size   = Extents(w, int(2 * w / 3))
        ext_down = self._down_btn.get_optimal_size()
        ext_up   = self._up_btn  .get_optimal_size()
        y1 = ext_down[1] + 1 # leave one pixel blank
        self._up_btn.position = Point(0, 0)
        self._up_btn.extents  = (self.extents[0], ext_up[1])
        y2 = self.extents[1] - ext_down[1] - 1
        self._down_btn.position = (0, y2 + 1)
        self._down_btn.extents  = (w, ext_down[1])
        self._thumb.rectangle = Rectangle( Point(0, y1), Extents(w, y2 - y1) )
        print("thumb rectangle: {}, {}".format(self._thumb.rectangle.position, self._thumb.rectangle.extents))
        ls = y2 - y1 # "slide" length
        lt = min(ls, int(ls * self._lengths[0] / self._lengths[1])) if self._lengths[1] > 0 else ls
        self._thumb.set_size( self.extents[0], lt )
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

    @property
    def percentage(self):
        return (self._thumb.position.y - self._thumb.rectangle.position.y) / self._thumb.rectangle.extents.h
        
    def line_up(self):
        self._thumb.move( Vector(0, -1) )
        self.do_value_changed()
    
    def line_down(self):
        #print("line_down")
        self._thumb.move( Vector(0, 1) )
        self.do_value_changed()
        
    def page_up(self):
        print("page_up()")
        self._thumb.move( Vector(0, -self._thumb.height) )
        self.do_value_changed()
    
    def page_down(self):
        print("page_down()")
        self._thumb.move( Vector(0,  self._thumb.height) )
        self.do_value_changed()
        
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
                self.do_value_changed()
                self.invalidate()
        elif isinstance(event, MouseButtonEvent):
            pos = event.position - parent_offset - self.position
            if event.button == 1 and event.state_is_pressed:
                if self._thumb.contains(pos):
                    self._thumb.start_dragging(pos)
                    return True
                elif self._thumb.rectangle.contains(pos):
                    if pos.y < self._thumb.position.y:
                        self.page_up()
                    else:
                        self.page_down()
                    return True
            elif event.button == 1 and event.state_is_released:
                if self._thumb.dragging:
                    self._thumb.stop_dragging()
                    return True
        elif isinstance(event, MouseWheelEvent):
            if self.hovered:
                self._thumb.move( - event.vector )
            return True
                    
        super().handle_event(event, parent_offset)

    def do_value_changed(self):
        self._position_changed.emit(self, self.percentage)