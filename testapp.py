import sys, os
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *

# Insert path of testee library
path = os.path.realpath(__file__)
path = os.path.dirname(path)
path = os.path.dirname(path)
path = os.path.dirname(path)
sys.path.insert(0, path)

from root_widget import RootWidget
from label import Label
from button import Button
from scrollbars import VerticalScrollbar
from container import Container
from geometry import BoundingBox

from application import Application # FIXME: make into real module, either of Pygwy or Pygwy platform module

# FIXME: use resources
thisdir = os.path.dirname(os.path.realpath(__file__))

# Experimental code

from geometry import Point, Extents

class MenuBarLayouter(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spacing = 5
        #self.minimal_element_size = Extents(0, 0)

    def get_bounding_box(self):

        w = 0 # TODO: take border into account
        max_ascender = max_descender = -10000
        for i, child in enumerate(self._children):
            bbox = child.get_bounding_box()
            if bbox.ascender  > max_ascender: max_ascender = bbox.ascender
            if bbox.descender > max_descender: max_descender = bbox.descender
            if i > 0: w += self.spacing
            w += bbox.w

        return BoundingBox(w, max_ascender, max_descender)

    def layout(self):

        bbox = self.get_bounding_box()
        y_base = (self.extents.h - bbox.h) // 2 + bbox.ascender
        x = 0 # TODO: start at border
        for child in self._children:
            #child.extents = child.get_optimal_size() | self.minimal_element_size
            cbb = child.get_bounding_box()
            child.position = Point(x, y_base - bbox.ascender)
            child.extents = Extents(cbb.w, cbb.h)
            x += child.extents.w + self.spacing
            
        super().layout() # will call layout() on children
        
class MyContainer(MenuBarLayouter, Container):
    
    def draw(self, canvas, offset):
        #print("MyContainer.draw()")
        
        pos = offset + self.position
        canvas.rectangle(pos.x, pos.y, self.extents.w, self.extents.h, [1, 1, 0.2, 1])
        
        super().draw(canvas, offset)

# TODO: this class is in early development, move into its own module as soon as it is ready for that

class MenuBar(MenuBarLayouter, Container): # TODO: derive from base class "Menu"
    
    def add_submenu(self, text):        
        sm = Button(caption = text)
        self.add_child(sm)
        return sm

    def layout(self):
        super().layout()
        
    def draw(self, canvas, offset):        
        pos = offset + self.position
        canvas.rectangle(pos.x, pos.y, self.extents.w, self.extents.h, [0.7, 0.7, 0.7, 1])
        super().draw(canvas, offset)

# RootWidget specialization

class MyRootWidget(RootWidget):
    
    # TODO: inherit this from a layouter class [not created yet]
    def layout(self):
        # TODO: quick and dirty: we only position the first child, assumed to be the menu
        self._children[0].position = Point(0, 0)
        self._children[0].extents = Extents(self.extents.w, self._children[0].get_bounding_box().h)
        super().layout()
    
# Application class 

class MyApp(Application):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def start(self):
    
        root_widget = MyRootWidget()

        menubar = MenuBar()
        root_widget.add_child(menubar)
        file = menubar.add_submenu("File")
        help = menubar.add_submenu("Help")
        
        cont1 = MyContainer()
        cont1.position = ( 50,  50)
        cont1.extents = (500, 200)
        cont1.minimal_element_size = Extents(0, 30)
        root_widget.add_child(cont1)
        
        btn1 = Button(caption="Click me!")
        #btn1.position = ( 10, 10)
        #btn1.extents  = (200, 50)
        btn1.clicked.subscribe( self._generic_click_handler )        
        cont1.add_child(btn1)

        btn2 = Button(caption="No, me!")
        btn2.clicked.subscribe( self._generic_click_handler )        
        cont1.add_child(btn2)

        #my_scrollbar = VerticalScrollbar(lengths=(10, 100))
        #my_scrollbar.position = (300, 100)
        #my_scrollbar.extents = (30, 200)
        #my_scrollbar.position_changed.subscribe(lambda source, value: print("new value: {}".format(value)))
        #root_widget.add_child(my_scrollbar)
        
        self.open_main_window(root_widget)
        
    def _generic_click_handler(self, widget):
        print("Click event sent from {}".format(widget))
        
    def init_gl(self):
        super().init_gl()
        
        glClearColor(0, 0.4, 1, 0)
       
    def cleanup_gl(self):
        super().cleanup_gl()
        
    def redraw(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Render the GUI
        # TODO: dirty, temporary: accessing protected, and itself temporary, _root_widget member
        self._root_widget.render()

        glFlush()
        
        # Present the display (not needed if single-buffer)
        #sdl2.SDL_GL_SwapWindow(window.window)

# MAIN ROUTINE ------------------------------------------------------

if __name__ == '__main__':
    app = MyApp()
    app.run()
