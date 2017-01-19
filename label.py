from numpy import *

from widget import Widget

class Label(Widget):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._txt_clr = (0, 0, 0, 1)
        self._bkg_clr = (0, 0, 0, 0)
        # FIXME: no or different default text
        self._text = "The quick brown fox jumped over the lazy dog."
        
    def layout(self):
        cbox = self.font.compute_control_box(self._text)
        # FIXME: for now, we just center the text, both horizontally and vertically
        self._x = (self.extents[0] - cbox.width ) // 2 - cbox.x_min
        self._y = (self.extents[1] - cbox.height) // 2 + cbox.y_max
        
    @property
    def background_color(self):
        return self._bkg_clr
        
    @background_color.setter
    def background_color(self, color):
        # TODO: check if alrady the right type
        self._bkg_clr = array(color, dtype=float32)
        
    @property
    def text_color(self):
        return self._txt_clr
        
    @text_color.setter
    def text_color(self, color):
        # TODO: check data type and convert to numpy.array() ?
        self._txt_clr = array(color, dtype=float32)
        
    def draw(self, canvas, offset):
        x = offset[0] + self.position[0]
        y = offset[1] + self.position[1]
        with canvas.clip(x, y, self._ext[0], self._ext[1]):
            if self._bkg_clr[3] != 0:
                canvas.rectangle(x, y, self._ext[0], self._ext[1], self._bkg_clr)
            canvas.draw_text(self.fonthandle, x + self._x, y + self._y, self._text, self._txt_clr)
        