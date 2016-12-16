# TODO: this module should be moved to Pygwy, as an SDL-specific implementation of the Application interface.

import sdl2.ext
import atexit
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from Pygwy import RootWidget
from Pygwy.sdl import wrap_event

class Application(object): # TODO: derive from interface defined in Pygwy

    def __init__(self):
        pass
        
    @property
    def root_widget(self): return self._root_widget
    
    def start(self):

        self._open_main_window()
        
        self.root_widget.layout()
        self.root_widget.set_extents(self.window.size) # TODO: support resizing!
        self.root_widget.update_view()      
        self.root_widget.init_graphics()

        self.window.show()

    def cleanup(self):
        pass # FIXME

    def define_gui(self, root_widget):
        """This is the callback that allows derived classes to define their GUI. Note that the OpenGL context is not yet active at this point."""
        pass
        
    def init_gl(self):
        """This method can be overridden by derived classes to do initialization when the OpenGL context has become available."""
        # FIXME: this should not belong to the application but to each window, as they could have different OpenGL contexts
        pass
        
    def cleanup_gl(self):
        """Override this to free OpenGL resources allocated in init_gl()."""
        pass
        
    def update_state(self):
        """This is the designated hook for update the application's internal state. [TODO: elaborate on this]"""
        # FIXME: call this method from somewhere!
        pass

    def update_windows(self):
        """This method redraws all the windows that belong to the application (for now, only one windows is supported)."""
    
        # TODO: support multiple windows
        self.redraw()

    def run(self):
        self.start()        
        running = True
        while running:
            events = sdl2.ext.get_events()
            for event in events:
                if event.type == sdl2.SDL_QUIT:
                    running = False
                    break
                else:
                    if event.type == sdl2.SDL_KEYDOWN and event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        running = False
                        break         
                    self.root_widget.handle_event( wrap_event(event) )
                    #if root_widget.must_redraw:
                    #    print("must_redraw")
                    #    evt = sdl2.SDL_Event()
                    #    evt.type = redraw_gui_event_id
                    #    sdl2.SDL_PushEvent(event)

            self.update_state()
            self.update_windows()
            
        self.cleanup_gl() # FIXME: belongs to window
        self.cleanup()
            
    def _open_main_window(self):
        # Create the window, prepare it for OpenGL
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER,  0) # Not useful in Windows 10
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE  , 24)
        #sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1);
        #sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES,16);
        #sdl2.SDL_GL_SetSwapInterval(1)

        self._root_widget = RootWidget()        
        self.define_gui(self._root_widget)
        
        self.window = sdl2.ext.Window("MSTSOGL Test App", size=(800, 600), 
            flags=sdl2.SDL_WINDOW_OPENGL|sdl2.SDL_WINDOW_FULLSCREEN|sdl2.SDL_WINDOW_MAXIMIZED)

        self.glctx = sdl2.SDL_GL_CreateContext(self.window.window)
        size = self.window.size
        glViewport(0, 0, size[0], size[1])
        
        self.init_gl()

    # Class initialization & cleanup
    
    def _cleanup_all():
        print("Application._cleanup_all()")
        sdl2.ext.quit()
        
    sdl2.ext.init()
    redraw_gui_event_id = sdl2.SDL_RegisterEvents(1)

    atexit.register( _cleanup_all )
    
