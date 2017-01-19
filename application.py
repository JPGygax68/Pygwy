# TODO: this module should be moved to Pygwy, as an SDL-specific implementation of the Application interface.

import sdl2.ext
import atexit
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
from root_widget import RootWidget
from sdl import wrap_event

class Application(object): # TODO: derive from interface defined in Pygwy

    def __init__(self):
        
        self._main_window = None

    def start(self):
        """Hook where windows should be created."""
        pass
        
    # TODO: replace with support for multiple windows

    def open_main_window(self, root_widget = None):

        if self._main_window is None: self._create_main_window(root_widget)
        
        self._root_widget.update_view()      
        self._root_widget.init_graphics()

        self._main_window.show()

    def cleanup(self):
        pass # FIXME

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
                elif event.type == sdl2.SDL_KEYDOWN:
                    if event.key.keysym.sym == sdl2.SDLK_ESCAPE:
                        running = False
                        break
                else:
                    # TODO: multiple windows -> multiple root widgets
                    self._root_widget.handle_event( wrap_event(event) )
                    #if _root_widget.must_redraw:
                    #    print("must_redraw")
                    #    evt = sdl2.SDL_Event()
                    #    evt.type = redraw_gui_event_id
                    #    sdl2.SDL_PushEvent(event)

            self.update_state()
            self.update_windows()
            
        self.cleanup_gl() # FIXME: belongs to window
        self.cleanup()
            
    # FIXME: replace with support for multiple windows    
    def _create_main_window(self, root_widget):
        # Create the window, prepare it for OpenGL
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DOUBLEBUFFER,  0) # Not useful in Windows 10
        sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_DEPTH_SIZE  , 24)
        #sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLEBUFFERS, 1);
        #sdl2.SDL_GL_SetAttribute(sdl2.SDL_GL_MULTISAMPLESAMPLES,16);
        #sdl2.SDL_GL_SetSwapInterval(1)

        self._root_widget = root_widget        
        self._main_window = sdl2.ext.Window("MSTSOGL Test App", size=(800, 600), 
            flags=sdl2.SDL_WINDOW_OPENGL|sdl2.SDL_WINDOW_FULLSCREEN|sdl2.SDL_WINDOW_MAXIMIZED)

        self.glctx = sdl2.SDL_GL_CreateContext(self._main_window.window)
        size = self._main_window.size
        glViewport(0, 0, size[0], size[1])
        
        self.init_gl()

    # Class initialization & cleanup
    
    def _cleanup_all():
        print("Application._cleanup_all()")
        sdl2.ext.quit()
        
    sdl2.ext.init()
    redraw_gui_event_id = sdl2.SDL_RegisterEvents(1)

    atexit.register( _cleanup_all )
