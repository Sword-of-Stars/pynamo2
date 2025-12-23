import sys
from array import array

import pygame
import moderngl

class ShaderContext():
    def __init__(self):
        self.ctx = moderngl.create_context()

        self.quad_buffer = self.ctx.buffer(data=array('f', [
            # position (x, y), uv coords (x, y)
            -1.0, 1.0, 0.0, 0.0,  # topleft
            1.0, 1.0, 1.0, 0.0,   # topright
            -1.0, -1.0, 0.0, 1.0, # bottomleft
            1.0, -1.0, 1.0, 1.0,  # bottomright
        ]))

        self.program = self.ctx.program(vertex_shader=vert_shader, fragment_shader=frag_shader)
        self.render_object = self.ctx.vertex_array(self.program, [(self.quad_buffer, '2f 2f', 'vert', 'texcoord')])

        self.time = 0

    def surf_to_texture(self,surf):
        tex = self.ctx.texture(surf.get_size(), 4)
        tex.filter = (moderngl.NEAREST, moderngl.NEAREST)
        tex.swizzle = 'BGRA'
        tex.write(surf.get_view('1'))
        return tex

    def update(self, display, ui): # eventually just use kwargs
        self.time += 1

        frame_tex = self.surf_to_texture(display)
        frame_tex.use(0)

        ui_tex = self.surf_to_texture(ui)
        ui_tex.use(1)

        self.program['tex'] = 0
        self.program['ui_surf'] = 1

        self.program['screen_size'].value = display.get_size()


        class Light:
            def __init__(self, pos, radius, intensity, color):
                self.pos = pos
                self.radius = radius
                self.intensity = intensity
                self.color = color

        myLight = Light((400.0, 300.0), 100.0, 0.2, (1.0, 1.0, 1.0))
        myLight2 = Light((100.0, 100.0), 200.0, 0.5, (1.0, 0, 0))

        lights = [myLight, myLight2]

        self.program["num_lights"] = len(lights)

        for i, light in enumerate(lights):
            self.program[f'lights[{i}].position'].value = light.pos
            self.program[f'lights[{i}].radius'].value = light.radius
            self.program[f'lights[{i}].intensity'].value = light.intensity
            self.program[f'lights[{i}].color'].value = light.color

        #self.program['time'] = self.time
        self.render_object.render(mode=moderngl.TRIANGLE_STRIP)
        
        pygame.display.flip()
        
        frame_tex.release()
        ui_tex.release()

vert_shader = '''
#version 330 core

in vec2 vert;
in vec2 texcoord;
out vec2 uvs;

void main() {
    uvs = texcoord;
    gl_Position = vec4(vert, 0.0, 1.0);
}
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform sampler2D ui_surf;
uniform float outRad;
uniform float inRad;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = inRad * textureSize;
    float outerRadius = outRad * textureSize;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength), textureColor.a);

    // Don't apply vignette to UI
    vec4 ui_color = texture(ui_surf, uvs);
    if (ui_color.a > 0) {
        f_color = ui_color;
  }
}
'''
'''
frag_shader = 
#version 330 core

uniform sampler2D tex;

in vec2 uvs;
out vec4 f_color;

void main() {
    // Calculate distance from center (assuming a centered vignette)
    vec2 center = vec2(0.5, 0.5);
    float distanceFromCenter = distance(uvs, center);

    // Adjust radii based on texture dimensions (assuming square texture)
    float textureSize = 1.0; // Replace with actual texture size if known
    float innerRadius = 0.2 * textureSize;
    float outerRadius = 0.7 * textureSize;

    // Calculate vignette strength
    float vignetteStrength = smoothstep(innerRadius, outerRadius, distanceFromCenter);

    // Apply vignette to texture color
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgb * (1.0 - vignetteStrength), textureColor.a);
  }
'''

frag_shader = '''
#version 330 core

uniform sampler2D tex;
uniform sampler2D ui_surf;

in vec2 uvs;
out vec4 f_color;

void main() {
   
    vec4 textureColor = texture(tex, uvs);
    f_color = vec4(textureColor.rgba);

    // Don't apply any effects to UI
    vec4 ui_color = texture(ui_surf, uvs);
    if (ui_color.a > 0) {
        f_color = ui_color;
  }
}
'''

frag_shader = """#version 330 core

#define MAX_LIGHTS 64

uniform sampler2D tex;
uniform sampler2D ui_surf;

uniform vec2 screen_size;   // (width, height) in pixels
uniform int num_lights;

struct PointLight {
    vec2 position;    // pixel-space position
    float radius;     // radius in pixels
    float intensity;  // brightness scalar
    vec3 color;       // normalized RGB
};

uniform PointLight lights[MAX_LIGHTS];

in vec2 uvs;
out vec4 f_color;

void main() {

    // Convert fragment to pixel space
    vec2 frag_px = uvs * screen_size;

    vec4 base_color = texture(tex, uvs);

    // UI pass-through
    vec4 ui_color = texture(ui_surf, uvs);
    if (ui_color.a > 0.0) {
        f_color = ui_color;
        return;
    }

    vec3 lighting = vec3(0.0);

    for (int i = 0; i < num_lights; i++) {
        PointLight light = lights[i];

        vec2 d = frag_px - light.position;
        float dist = length(d);

        if (dist >= light.radius) continue;

        // Gaussian falloff (smooth, no hard edge)
        float x = dist / light.radius;
        float attenuation = exp(-x * x * 4.0);

        lighting += light.color * light.intensity * attenuation;
    }

    vec3 lit_color = base_color.rgb + lighting;

    // Clamp to avoid overflow
    lit_color = min(lit_color, vec3(1.0));

    f_color = vec4(lit_color, max(base_color.a, length(lighting)));
}
"""