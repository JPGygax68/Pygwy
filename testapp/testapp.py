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

from Pygwy import RootWidget, Label, Button, VerticalScrollbar, Container

from application import Application # FIXME: make into real module, either of Pygwy or Pygwy platform module

# FIXME: use resources
thisdir = os.path.dirname(os.path.realpath(__file__))

# Experimental code

from Pygwy.geometry import Point, Extents

class MyLayouter(Container):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.spacing = 5
        self.minimal_element_size = Extents(0, 0)
        
    def get_optimal_size(self):

        minsz = Extents(0, 0)
        for child in self._children:
            child.extents = child.get_optimal_size() | self.minimal_element_size
            minsz = Extents(minsz.w + child.extents.w, max(minsz.h, child.extents.h))
    
    def layout(self):
        
        x = 0 # TODO: start at border
        for child in self._children:
            child.extents = child.get_optimal_size() | self.minimal_element_size
            print("child.extents: {}".format(child.extents))
            child.position = Point(x, (self.extents.h - child.extents.h) // 2)
            x += child.extents.w + self.spacing
            
        super().layout() # will call layout() on children
        
class MyContainer(MyLayouter, Container):
    
    def draw(self, canvas, offset):
        #print("MyContainer.draw()")
        
        pos = offset + self.position
        canvas.rectangle(pos.x, pos.y, self.extents.w, self.extents.h, [1, 1, 0.2, 1])
        
        super().draw(canvas, offset)
        
class MenuBar(Container):
    
    def layout(self):
        self.position = Point(0, 0)
        print("MenuBar.layout(), parent extents: {}, parent: {}".format(self.parent.extents, self.parent))
        self.extents = Extents(self.parent.extents.w, 20) # TODO: compute height from direct children
        
    def draw(self, canvas, offset):        
        pos = offset + self.position
        #print("Menubar extents: {}".format(self.extents))
        canvas.rectangle(pos.x, pos.y, self.extents.w, self.extents.h, [0.7, 0.7, 0.7, 1])
        super().draw(canvas, offset)
        
# Application class 

class MyApp(Application):
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def define_gui(self, root_widget):
        
        menubar = MenuBar()
        root_widget.add_child(menubar)
        
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
        self.root_widget.render()

        glFlush()
        
        # Present the display (not needed if single-buffer)
        #sdl2.SDL_GL_SwapWindow(window.window)

# MAIN ROUTINE ------------------------------------------------------

if __name__ == '__main__':
    app = MyApp()
    app.run()
