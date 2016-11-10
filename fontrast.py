import os
import freetype as ft
import numpy

# FIXME: use resources
thisdir = os.path.dirname(os.path.realpath(__file__))

# Unicode ranges    
BASIC_LATIN = (0x20, 0x7F)
PRIVATE_USE = (0xE000, 0xE000 + 6400)
    
class GlyphIndex:
    """ The GlyphIndex class associates codepoints with glyph indices through a sparse list.
        Note that the indices are not actually stored: rather, they are defined to be the 
        sequential positions in the sparse list. Thus, GlyphIndex is actually an ordered
        sparse set.
        To ensure that indices do not change unexpectedly, it is forbidden to add codepoints
        after the seal() method has been called, and conversely, lookups via lookup() are
        forbidden before that point.
    """
    
    # The index consists of a list of ranges, represented by tuples:
    #   0: first codepoint
    #   1: last+1 codepoint
    # => in other words, the tuple specifies a half-open range of codepoints.

    def __init__(self):
        self.ranges = []
        
    def add_codepoints(self, start, end):
        """Add a range (half-open) of Unicode codepoints to the index."""
        
        # Find where to insert the new range
        i = 0
        while i < len(self.ranges): 
            if start <= self.ranges[i][1]: break
            i += 1
        #print("i: {}".format(i))
        
        # Not in any of the existing ranges ?
        if i == len(self.ranges):
            # Append a new range
            self.ranges.append([ start, end ])
        else:
            #print("New range {}:{} begins before or inside existing range, or appends to one".format(start,end))          
            
            # Find last of the ranges we're going to replace (in case the new range spans multiple existing ones)
            j = i
            while j < (len(self.ranges) - 1) and end >= self.ranges[j][0]: j = j + 1
            
            # Compute the new end-of-range codepoint
            new_end = max(end, self.ranges[j][1])
            
            # Erase the ranges we're replacing
            del self.ranges[i + 1 : j + 1]
            
            # Reuse the existing range
            self.ranges[i] = (self.ranges[i][0], new_end)
            #print("new range {}: {}:{}".format(i, self.ranges[i][0], self.ranges[i][1]))
            
    def seal(self):
        """"MUST be called once all codepoint ranges have been added, and before performing
        any lookups."""
        
        self.sealed = True
        
    def lookup(self, codepoint):
        """Get the ordinal index of the specified codepoint. Will raise KeyError if the codepoint 
        is not contained in the index."""
        
        if not self.sealed: 
            raise Exception("GlyphIndex.lookup() called before index was sealed. Call seal() when done adding glyphs.")
        base = 0
        for rng in self.ranges:
            #print("rng: {}, codepoint: {}".format(rng, codepoint))
            if (rng[0] <= codepoint and codepoint < rng[1]):
                return base + codepoint - rng[0]
            base += rng[1] - rng[0]
                
        raise KeyError("GlyphIndex instance does not contain the specified codepoint ({})".format(codepoint))
            
    @property
    def count(self):
        n = 0
        for rng in self.ranges: n += rng[1] - rng[0]
        return n
        
    def __iter__(self):
        for rng in self.ranges:
            for ch in range(rng[0], rng[1]):
                yield ch
        
    def __str__(self):
        s = ""
        for rng in self.ranges:
            s += "[" + str(rng[0]) + ", " + str(rng[1]) + "]"
        return s
        
class ControlBox:

    @staticmethod
    def from_glyph_records(records, glyph_index):
        r = records; b = 7 * glyph_index
        return ControlBox(r[b+0], r[b+1], r[b+2], r[b+3], r[b+4], r[b+5])
           
    def __init__(self, x_min = 32767, x_max = -32768, y_min = 32767, y_max = -32768, adv_x = 0, adv_y = 0):
        self.x_min = x_min; self.x_max = x_max; self.y_min = y_min; self.y_max = y_max
        self.adv_x = adv_x; self.adv_y = adv_y
        
    @property
    def width(self):
        return self.x_max - self.x_min
        
    @property
    def height(self):
        return self.y_max - self.y_min
        
    def __str__(self):
        return "x_min: {}, y_min: {}, x_max: {}, y_max: {}".format(self.x_min, self.y_min, self.x_max, self.y_max)
        
class _RasterizedFont:
    """ This class encapsulates a font that has been rasterized for a given pixel size. Members:
        glyph_recs:
            A numpy array of int16 values; each group of 7 of these values (= one "glyph descriptor") contains 
            the information needed to render the corresponding glyph:
            0 "x_min":       position of the left-most pixel of the glyph, relative to the glyph origin
            1 "x_max":       ditto right-most pixel
            2 "y_min":       ditto bottom pixel
            3 "y_max":       ditto top-most pixel
            4 "adv_x":       where to place the origin of the next character (relative to the origin of this one)
            5 "adv_y":       ditto for vertical axis (for vertical scripts only)
            6 "first_pixel": ordinal position of first pixel in the (one-dimensional) pixel-buffer (see below)
        glyph_index: 
            A GlyphIndex object (to look up glyph indices from Unicode codepoints)
        pixel_buffer:
            The pixel buffer itself (bytearray)
        
        NOTE: while a signed 16-bit integer should be enough to contain the first 6 fields the the glyph descriptor
            pseudo-structure, it may be too small to specify all the starting pixel offsets for large glyph sets
            (e.g. such as would be needed for asian text) and/or glyph sets rasterized for large pixel sizes.
            It is very likely that a future version will combine two 16-bit fields (thereby increasing the size 
            of the glyph record pseudo-struct to 8 values, unless one of the adv values can be recycled by keeping
            that information elsewhere - it does not have to be repeated for each glyph).
    """        
    
    def compute_control_box(self, text):
        """Compute the "control box" for a given Unicode string."""
        
        cbox = ControlBox()
        
        x = 0 # TODO: support vertical scripts!
        y = 0
        for ch in text:
            cb = ControlBox.from_glyph_records(self.glyph_recs, self.glyph_index.lookup(ord(ch)))
            if x + cb.x_min < cbox.x_min: cbox.x_min = x + cb.x_min
            if x + cb.x_max > cbox.x_max: cbox.x_max = x + cb.x_max
            if y + cb.y_min < cbox.y_min: cbox.y_min = y + cb.y_min
            if y + cb.y_max > cbox.y_max: cbox.y_max = y + cb.y_max
            x += cb.adv_x; y += cb.adv_y
            
        return cbox
    
class FontRasterizer:
    
    # TODO: many more (http://jrgraphix.net/research/unicode_blocks.php)
    

    def __init__(self, **kwargs):
        global thisdir
        #self.dflt_font = self._rasterize_font(os.path.join(thisdir, "fonts/LiberationSans-Regular.ttf"), 16)
        #print("Default font glyph index: {}".format(self.dflt_font[1]))
        
    def rasterize_font(self, path, pixel_size, cp_range = BASIC_LATIN):
        """Rasterizes a font for a given pixel size. Returns Rasterization instance (see above)."""
        
        # TODO: optional (keyword?) parameter for "index", for font files containing more than one glyph set
        
        face = ft.Face(path)
        face.select_charmap(ft.FT_ENCODING_UNICODE)
        face.set_pixel_sizes(0, pixel_size)
        
        glyph_index = GlyphIndex()
        ch = cp_range[0] - 1
        while ch < cp_range[1]:
            ch, glindex = face.get_next_char(ch, 0)
            glyph_index.add_codepoints(ch, ch + 1)
        #glyph_index.add_codepoints(cp_range[0], cp_range[1] + 1)
        glyph_index.seal()
        print("glyph_index: {}".format(glyph_index))
        
        # Construct the pixel buffer and glyph descriptor table
        print("Glyph count: {}".format(glyph_index.count))
        pixel_buffer = bytearray()
        glyph_recs = numpy.empty(7 * glyph_index.count, dtype=numpy.int16) # list of glyph descriptors
        i_gr = 0
        for ch in glyph_index:
            #print("ch = {}".format(ch))
            #print("Glyph #{} advance: {}".format(i, face.get_advance(i, 0) / 64))
            face.load_char(chr(ch), ft.FT_LOAD_RENDER | ft.FT_LOAD_TARGET_NORMAL)
            gs = face.glyph # glyph slot
            #gs.render_glyph()
            bm = face.glyph.bitmap
            #print("rows: {}, cols: {}, left: {}, top: {}".format(gs.bitmap.rows, gs.bitmap.width, gs.bitmap_left, gs.bitmap_top))
            # Compute control box
            glyph_recs[i_gr + 0] = gs.bitmap_left
            glyph_recs[i_gr + 1] = gs.bitmap.width + gs.bitmap_left
            glyph_recs[i_gr + 2] = gs.bitmap_top - gs.bitmap.rows
            glyph_recs[i_gr + 3] = gs.bitmap_top
            glyph_recs[i_gr + 4] = gs.advance.x >> 6
            glyph_recs[i_gr + 5] = gs.advance.y >> 6
            glyph_recs[i_gr + 6] = len(pixel_buffer)
            i_gr += 7
            # Append pixel_buffer to buffer
            #print("Width: {}, Rows: {}, mode: {}, buffer: {}".format(bm.width, bm.rows, bm.pixel_mode, bm.buffer))
            pixel_buffer.extend(bm.buffer)
        
        # We have our rasterization, wrap and return it
        rst = _RasterizedFont()
        rst.pixel_size = pixel_size
        rst.glyph_recs = glyph_recs
        rst.glyph_index = glyph_index
        rst.pixel_buffer = pixel_buffer
        return rst
        