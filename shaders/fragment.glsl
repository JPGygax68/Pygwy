#version 430

uniform int             vp_width;
uniform int             vp_height;
uniform vec4            color;
uniform sampler2DRect   sampler;
uniform int             render_mode;
uniform ivec2           offset;             // when rendering images: top-left corner inside image
uniform float           point_size;
uniform samplerBuffer   font_pixels; 
uniform isamplerBuffer  glyph_descriptors;  // TODO: replace this with a UBO for speed ?

in vec2 texel_position;
flat in uint frag_glyphindex;

out vec4 fragment_color;

void main() {

    // Apply single color
    if (render_mode == 1) {

        fragment_color = color;
    }
    // Image pasting
    else if (render_mode == 2) {

        ivec2 tex_size = textureSize(sampler, 0);
        fragment_color = texelFetch(sampler, (ivec2(texel_position) + offset) % tex_size);
    }
    // Glyph rendering
    else if (render_mode == 3) {

        int descr_base = int(8 * frag_glyphindex);
        int x_min      = texelFetch(glyph_descriptors, descr_base + 0).r;
        int x_max      = texelFetch(glyph_descriptors, descr_base + 1).r;
        int y_min      = texelFetch(glyph_descriptors, descr_base + 2).r;
        int y_max      = texelFetch(glyph_descriptors, descr_base + 3).r;
        int pbase_low  = texelFetch(glyph_descriptors, descr_base + 6).r;
        int pbase_high = texelFetch(glyph_descriptors, descr_base + 7).r;
        int pixel_base = (pbase_low < 0 ? 256 + pbase_low : pbase_low) + 256 * pbase_high;
        
        int w = x_max - x_min, h = y_max - y_min;
        
        float x = (gl_PointCoord.s - 0.5) * point_size;
        float y = - (gl_PointCoord.t - 0.5) * point_size; // bottom-up
        
        float xx = x - x_min, yy = y_max - y;
        if (xx >= 0 && xx < float(w) && yy >= 0 && yy < float(h))
        {
          int col = int(xx), row = int(yy);
          float v = texelFetch(font_pixels, pixel_base + row * w + col).r;        
        
          fragment_color = vec4(color.rgb, color.a * v); // vec4(color.rgb, 1); // color.a * v);
        }
        else {
          fragment_color = vec4(0, 0, 0, 0);
          //fragment_color = vec4(gl_PointCoord.st, 0, 1);
        }
    }
}