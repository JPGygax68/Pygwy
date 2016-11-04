#version 430

// Viewport width and height
uniform int           vp_width;
uniform int           vp_height;
uniform ivec2         position;
uniform int           render_mode;
uniform ivec4         glyph_cbox;

uniform mat4          transform;

in  vec2 vertex_position;
in  uint glyph_index;

out vec2 texel_position;
flat out uint frag_glyphindex;
out float point_size;

void main() {

    if (render_mode == 1 || render_mode == 2) {

        vec4 vp = transform * vec4(vertex_position, 0, 1);
        
        gl_Position = vec4(2 * vp.x / float(vp_width) - 1, - 2 * vp.y / float(vp_height) + 1, 0, 1);
        
        texel_position = vertex_position.xy - position;
    }
    else if (render_mode == 3) {

        vec4 vp = vec4(vertex_position, 0, 1);
        gl_Position = vec4(2 * vp.x / float(vp_width) - 1, - 2 * vp.y / float(vp_height) + 1, 0, 1);
        
        frag_glyphindex = glyph_index;        
    }
}
