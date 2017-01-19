# FIXME: this is the OpenGL implementation of the Canvas interface and therefore belongs into its own module; also, a separate module with the interface needs to be created (and used here!)

import os
import OpenGL
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy
import ctypes
from pyrr import Quaternion, Matrix44, Vector3

# FIXME: use resources
thisdir = os.path.dirname(os.path.realpath(__file__))

# Two triangles to form a rectangle, size 1x1
RECTANGLE_VERTICES = [ 0,0, 1,0, 1,1,   1,1, 0,1, 0,0]
#RECTANGLE_VERTICES = numpy.array(RECTANGLE_VERTICES, dtype=numpy.float32)
RECTANGLE_VERTICES = arrays.ArrayDatatype.asArray(RECTANGLE_VERTICES, typeCode = GL_FLOAT)

class _FontHandle:
    """Represents a RasterizedFont processed for use by the canvas."""
    pass
    
class Canvas:
    """OpenGL implementation of the Pygwy Canvas concept."""
    
    class Clipper:
    
        def __init__(self, canvas, x, y, w, h):
            self._canvas = canvas
            self._x = x
            self._y = y
            self._w = w
            self._h = h
            
        def __enter__(self):
            #print("Entering Clipper: {}, {}, {}, {}; extents = {}".format(self._x, self._y, self._w, self._h, self._canvas.extents))
            if len(self._canvas._clipper_stack) == 0:
                glEnable(GL_SCISSOR_TEST) 
            self._canvas._clipper_stack.append( self )
            glScissor(self._x, self._canvas.extents.h - self._y - self._h, self._w, self._h)
            
        def __exit__(self, type, value, traceback):
            #print("Leaving clipper")
            self._canvas._clipper_stack.pop()
            if len(self._canvas._clipper_stack) == 0:
                glDisable(GL_SCISSOR_TEST)
            else:
                cl = self._canvas._clipper_stack[-1]
                glScissor(cl._x, self._canvas.extents.h - cl._y, cl._w, cl._h)
            
    def __init__(self):
        self._font_cache = {}
        self._clipper_stack = []
        
    def init(self):
        """Must be called with an active OpenGL context; that same context will also need to be active
            whenever any of the drawing methods is called."""
            
        global thisdir
        # Create the shader program
        self.program = glCreateProgram()
        vertex_shader = glCreateShader(GL_VERTEX_SHADER)
        glShaderSource(vertex_shader, open(os.path.join(thisdir, "shaders/vertex.glsl"), "r"))
        glAttachShader(self.program, vertex_shader)
        fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
        glShaderSource(fragment_shader, open(os.path.join(thisdir, "shaders/fragment.glsl"), "r"))
        glCompileShader(fragment_shader)
        if not glGetShaderiv(fragment_shader, GL_COMPILE_STATUS):
            raise SystemError("GUI: could not compile fragment shader: {}\n".format(glGetShaderInfoLog(fragment_shader)))
        #print(glGetShaderInfoLog(fragment_shader))
        glAttachShader(self.program, fragment_shader)
        glLinkProgram(self.program)
        glDeleteShader(vertex_shader)
        glDeleteShader(fragment_shader)
        if glGetProgramiv(self.program, GL_LINK_STATUS) != GL_TRUE:
            raise SystemError("Pygwy: failed to get shader program info log: {0}".format(glGetProgramInfoLog(self.program)))
        
        # Obtain the locations of the uniforms
        uniforms = ["vp_width", "vp_height", "render_mode", "transform", "color", "point_size", "font_pixels", "glyph_descriptors"]
        self.uniforms = { name: glGetUniformLocation(self.program, name) for name in uniforms }
        #print("Uniforms: {}".format(self.uniforms))
        # ... and of the vertex attributes
        attributes = ["vertex_position", "glyph_index"]
        self.attributes = { name: glGetAttribLocation(self.program, name) for name in attributes }

        # Create a vertex array object to draw simple rectangles
        self.rectangle_vao = glGenVertexArrays(1)
        glBindVertexArray(self.rectangle_vao)
        self.rect_vert_buf = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.rect_vert_buf)
        data_size = arrays.ArrayDatatype.arrayByteCount(RECTANGLE_VERTICES)
        glBufferData(GL_ARRAY_BUFFER, data_size, RECTANGLE_VERTICES, GL_STATIC_DRAW)
        glVertexAttribPointer(self.attributes['vertex_position'], 2, GL_FLOAT, False, 0, ctypes.c_void_p(0))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)

        # Another vertex array object to draw text
        self.text_vao = glGenVertexArrays(1)
        glBindVertexArray(self.text_vao)
        self.text_vert_buf, self.text_glyphindex_buf = glGenBuffers(2)
        glBindBuffer(GL_ARRAY_BUFFER, self.text_vert_buf)
        glVertexAttribPointer(self.attributes['vertex_position'], 2, GL_FLOAT, False, 0, ctypes.c_void_p(0))
        glBindBuffer(GL_ARRAY_BUFFER, self.text_glyphindex_buf)
        glVertexAttribIPointer(self.attributes['glyph_index'], 1, GL_UNSIGNED_INT, 0, ctypes.c_void_p(0))
        glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
        #print("Point size range: {}".format(glGetFloatv(GL_ALIASED_POINT_SIZE_RANGE)))
        
    def cleanup():
        # TODO: release font resources
        pass
        
    def set_extents(self, w, *h):
        """Must be called whenever the size of the display's client area has changed."""
        
        self.extents = (w, *h) if h else w

    def register_font(self, font):
        """Registers a RasterizedFont for use by this canvas instance, returning an opaque value (a handle)
        that must be specified when calling text-rendering methods.
        Note: the canvas need not necessarily be "entered" (using the "with" statement) for register_font() 
        to work, however the OpenGL context associated with this canvas must be active."""

        handle = self._font_cache.get(font, None)
        
        if handle:
            return handle
            
        else:
            handle = _FontHandle()
            handle.font = font
            
            # Upload data for default font
            # Upload bitmap for default font as buffer object, and bind that to a texture object
            handle.bitmap_buf = glGenBuffers(1)
            glBindBuffer(GL_TEXTURE_BUFFER, handle.bitmap_buf)
            print("font pixel buffer size: {}", len(font.pixel_buffer))
            glBufferStorage(GL_TEXTURE_BUFFER, len(font.pixel_buffer), font.pixel_buffer, 0)
            handle.texture = glGenTextures(1)
            glBindTexture(GL_TEXTURE_BUFFER, handle.texture)
            glTexBuffer(GL_TEXTURE_BUFFER, GL_R8, handle.bitmap_buf)
            glBindTexture(GL_TEXTURE_BUFFER, 0)
            
            # Do the same for the glyph records
            handle.glyphrecs_buf = glGenBuffers(1)
            glBindBuffer(GL_TEXTURE_BUFFER, handle.glyphrecs_buf)
            #print("glyph_recs size: {}", font.glyph_recs.nbytes)
            glBufferStorage(GL_TEXTURE_BUFFER, font.glyph_recs.nbytes, font.glyph_recs, 0)
            handle.glyphrecs_tex = glGenTextures(1)
            glBindTexture(GL_TEXTURE_BUFFER, handle.glyphrecs_tex)
            glTexBuffer(GL_TEXTURE_BUFFER, GL_R16I, handle.glyphrecs_buf)
            glBindBuffer(GL_TEXTURE_BUFFER, 0)
            glBindTexture(GL_TEXTURE_BUFFER, 0)
            
            # Store handle in cache
            self._font_cache[font] = handle
            
        return handle
        
    def rectangle(self, x, y, w, h, color):
        """Draw a filled (borderless) rectangle. The color must be specified as an (R,G,B,A) tuple."""
        
        glUniform1i(self.uniforms.get("render_mode"), 1)
        #matrix = Matrix44.identity()
        matrix = Matrix44.from_translation(Vector3([x, y, 0])) #* matrix
        matrix = Matrix44.from_scale(Vector3([w, h, 1])) * matrix
        matrix = numpy.array(matrix, numpy.float32)
        #matrix = arrays.ArrayDatatype.asArray(matrix, GL_FLOAT)
        #print("matrix: {}".format(matrix))
        glUniformMatrix4fv(self.uniforms.get('transform'), 1, False, matrix)
        color = numpy.array(color, numpy.float32)
        #color = arrays.ArrayDatatype.asArray(color, GL_FLOAT)
        #print("color: {}".format(color))
        glUniform4fv(self.uniforms.get('color'), 1, color)
        glBindVertexArray(self.rectangle_vao)
        glEnableVertexAttribArray(self.attributes.get('vertex_position'))
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

    def draw_text(self, fhandle, x, y, text, color, **kwargs):
        """Draw text at the specified position (origin of the first character)."""

        # IMPORTANT NOTE: the current implementation uses point sprites to render the characters.
        # Officially, OpenGL says that point sprites are clipped entirely when their origin is
        # outside the clipping volume. When tested on a GTX 970 card however, that was not the
        # case. If however an OpenGL implementation chooses to enforce that rule (which was 
        # overturned for the OpenGL ES specification), that would probably make this approach
        # essentially useless.
        # If that is the case, this article: http://stackoverflow.com/a/17400234/754534 has
        # alternative solutions.

        font = fhandle.font
        
        # Prepare glyph indices and coordinates
        vertices = []
        indices = []
        for ch in text:
            index = font.glyph_index.lookup(ord(ch))
            adv_x = font.glyph_recs[8*index + 4]
            adv_y = font.glyph_recs[8*index + 5]
            vertices.extend( [x, y] )
            indices.append( index )
            x += adv_x
            y += adv_y

        # Upload the positions and glyph indices
        vertices = numpy.array(vertices, numpy.float32)
        glBindBuffer(GL_ARRAY_BUFFER, self.text_vert_buf)
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_DYNAMIC_DRAW)
        indices = numpy.array(indices, numpy.uint)
        glBindBuffer(GL_ARRAY_BUFFER, self.text_glyphindex_buf)
        glBufferData(GL_ARRAY_BUFFER, indices.nbytes, indices, GL_DYNAMIC_DRAW)
        glBindBuffer(GL_ARRAY_BUFFER, 0)

        # Draw the glyphs as point sprites
        glActiveTexture(GL_TEXTURE0)
        glBindTexture(GL_TEXTURE_BUFFER, fhandle.texture)
        glActiveTexture(GL_TEXTURE1)
        glBindTexture(GL_TEXTURE_BUFFER, fhandle.glyphrecs_tex)
        glActiveTexture(GL_TEXTURE0)
        glBindVertexArray(self.text_vao)
        glEnableVertexAttribArray(self.attributes.get('vertex_position'))
        glEnableVertexAttribArray(self.attributes.get('glyph_index'))
        glUniform1i(self.uniforms.get('render_mode'), 3)
        glEnable(GL_POINT_SPRITE)
        point_size = 2 * font.pixel_size # twice the pixel size, just to be sure 
        # TODO: enable GL_PROGRAM_POINT_SIZE and set this from the vertex shader ?
        #   Doing so would required doing the lookups in the vertex shader instead of the fragment shader though.
        glPointSize(point_size)
        glUniform1f(self.uniforms.get('point_size'), point_size)
        glUniform4fv(self.uniforms.get('color'), 1, color)
        glDrawArrays(GL_POINTS, 0, len(indices))
            
        #glBindBuffer(GL_ARRAY_BUFFER, 0)
        glBindVertexArray(0)
        
    def clip(self, x, y, w, h):
        return Canvas.Clipper(self, x, y, w, h)
        
    def __enter__(self):
        
        # TODO: make state saving/restoring overridable/customizable, as it can be expensive
        
        # State that cannot be save via PushAttrib
        self.saved_state = {
            'program': glGetInteger(GL_CURRENT_PROGRAM),
        }
        
        # https://www.opengl.org/sdk/docs/man2/xhtml/glPushAttrib.xml
        glPushAttrib(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
        glDisable(GL_DEPTH_TEST)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        
        glUseProgram(self.program)
        #print("Uniforms: {}".format(self.uniforms))
        glUniform1i(self.uniforms.get('vp_width') , self.extents.w)
        glUniform1i(self.uniforms.get('vp_height'), self.extents.h)
        glUniform4f(self.uniforms.get('color'), 0, 0, 0, 1) # 1, numpy.array((0, 0, 0, 1)))
        glUniform1i(self.uniforms.get('font_pixels'), 0) # texture unit 0 for font pixels
        glUniform1i(self.uniforms.get('glyph_descriptors'), 1) # texture unit 1 for glyph descriptors
        
    def __exit__(self, type, value, traceback):

        glPopAttrib()
        glUseProgram(self.saved_state["program"])
        #if self.saved_state["depth_test"]: glEnable(GL_DEPTH_TEST)
