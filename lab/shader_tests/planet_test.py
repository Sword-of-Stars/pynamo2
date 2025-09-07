import pygame, sys
from shaders import ShaderContext
from noise import snoise3
import numpy as np
import moderngl


WIDTH, HEIGHT = 800,600

pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT),  pygame.OPENGL | pygame.DOUBLEBUF)
display = pygame.Surface((WIDTH, HEIGHT))
ui_surf = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)

ctx = ShaderContext()

clock = pygame.time.Clock()

# 1) find distance from center of screen
# 2) pull noise texture value from noise 3D

def create_noise_texture(ctx, size, scale=0.5):
    # Create a 3D array for noise data
    noise_data = np.zeros((size, size, size), dtype=np.float32)

    for z in range(size):
        for y in range(size):
            for x in range(size):
                # Generate Perlin noise for the coordinate (x, y, z)
                noise_value = snoise3(x / scale, 
                                       y / scale, 
                                       z / scale, 
                                       octaves=1, 
                                       persistence=1, 
                                       lacunarity=2.0)
                
                # Normalize to [0, 1] range
                noise_data[x, y, z] = (noise_value + 1) / 2.0

    # Reshape the noise_data to a flat 1D array for the texture
    noise_data_flat = noise_data.flatten()

    print(noise_data_flat.shape)  # Should be (size * size * size,)

    # Create a 3D texture (size, size, size) with 1 component (grayscale)
    texture = ctx.texture3d((size, size, size), 1, noise_data_flat.tobytes())

    # Set texture filtering and wrapping options
    texture.filter = (moderngl.LINEAR, moderngl.LINEAR)

    return texture

texture3d = create_noise_texture(ctx.ctx, 100)

while True:
    clock.tick(60)

    display.fill((0,0,0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    ctx.update(display, ui_surf, texture3d)


    
