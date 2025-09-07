import numpy as np
import moderngl
from noise import snoise3
from shaders import ShaderContext

import pygame

WIDTH, HEIGHT = 800,600

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((WIDTH, HEIGHT))
ui_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

ctx = ShaderContext()

def create_noise_texture(ctx, size, scale=1.0):
    # Create a 3D array for noise data
    noise_data = np.zeros((size, size, size), dtype=np.float32)

    for z in range(size):
        for y in range(size):
            for x in range(size):
                # Generate Perlin noise for the coordinate (x, y, z)
                noise_value = snoise3(x / scale, 
                                       y / scale, 
                                       z / scale, 
                                       octaves=4, 
                                       persistence=0.5, 
                                       lacunarity=2.0)
                noise_data[x, y, z] = (noise_value + 1) / 2  # Normalize to [0, 1]

    # Now we need to prepare the data for the texture array.
    # Reshape the noise_data to flatten the 3rd dimension (depth)
    noise_data_flat = noise_data.transpose(2, 0, 1).reshape(size, size * size).astype(np.float32)

    # Create a 2D texture array (width, height, depth)
    texture = ctx.texture_array((size, size, size), 4, noise_data_flat.tobytes())

    # Set texture filtering and wrapping options
    #stexture.filter = (moderngl.LINEAR, moderngl.LINEAR)


    return texture

create_noise_texture(ctx.ctx, 100)