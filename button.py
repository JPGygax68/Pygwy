from . widget import Widget
from . clickable import Clickable

class Button(Clickable, Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        #self._cap_clr = (0, 0, 0, 1)
        #self._face_clr_ = (0.5, 0.5, 0.5, 1)
        self._caption = "Button"
        
    def layout(self):
        cbox = self.font.compute_control_box(self._caption)
        # FIXME: for now, we just center the text, both horizontally and vertically
        self._x = (self.extents[0] - cbox.width ) // 2 - cbox.x_min
        self._y = (self.extents[1] - cbox.height) // 2 + cbox.y_max
        
    @property
    def face_color(self):
        if self.hovered:
            return (0.6, 0.6, 0.6, 1)
        else:
            return (0.5, 0.5, 0.5, 1)
        
    @property
    def caption_color(self):
        return (0, 0, 0, 1)
        
    @face_color.setter
    def face_color(self, color):
        # TODO: check if alrady the right type
        self._face_clr = array(color, dtype=float32)
        
    @caption_color.setter
    def caption_color(self, color):
        # TODO: check data type and convert to numpy.array() ?
        self._cap_clr = array(color, dtype=float32)
             
    #def handle_event(self, event, offset):
    #    #print("Button.handle_event()")
    #    return super().handle_event(event, offset)

    def draw(self, canvas, offset):
        x = offset[0] + self.position[0]
        y = offset[1] + self.position[1]
        with canvas.clip(x, y, self._ext[0], self._ext[1]):
            clr = self.face_color
            if clr[3] != 0: canvas.rectangle(x, y, self._ext[0], self._ext[1], clr)
            canvas.draw_text(self.fonthandle, x + self._x, y + self._y, self._caption, self.caption_color)
