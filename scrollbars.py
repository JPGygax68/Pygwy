from . container import Container
from . root_widget import RootWidget
from . button import Button

class VerticalScrollbar(Container):
    
    def __init__(self, *args, lengths = (0, 0), **kwargs):
        # TODO: set lengths here, or define extra property ?
        super().__init__(*args, **kwargs)
        self._lengths = lengths
        self._up_btn   = Button(caption = '\uE0BA')
        self._down_btn = Button(caption = '\uE5C5')
        self.add_child(self._up_btn)
        self.add_child(self._down_btn)

    def layout(self):
        #print("VerticalScrollbar.layout()")
        self._up_btn.font   = self.root_widget.default_icon_font
        self._down_btn.font = self.root_widget.default_icon_font
        down_btn_size = self._down_btn.get_optimal_size()
        up_btn_size   = self._up_btn  .get_optimal_size()
        self._up_btn  .position = (0, 0)
        self._down_btn.position = (0, self.extents[1] - down_btn_size[1])
        w = max(down_btn_size[0], up_btn_size[0])
        w += 10
        self._up_btn.extents   = (w, up_btn_size  [1] + 10)
        self._down_btn.extents = (w, down_btn_size[1] + 10)
        super().layout() # call layout() on children (buttons)
        
    def init_graphics(self, canvas):
        #print("VerticalScrollbar.init_graphics()")
        super().init_graphics(canvas)
        
    def update_view(self):
        # TODO: implement this: thumb position
        pass
        
    def draw(self, canvas, offset):
        #print("VerticalScrollbar.draw()")
        # Draw children
        super().draw(canvas, offset)
