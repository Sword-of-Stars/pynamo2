import pygame
import sys
import numpy as np
from noise import snoise3
import moderngl
from PIL import Image

# Constants
WIDTH, HEIGHT = 800, 600

# Initialize pygame
pygame.init()
pygame.display.set_mode((WIDTH, HEIGHT), pygame.OPENGL | pygame.DOUBLEBUF)

# Create a ModernGL context
ctx = moderngl.create_context()

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

    # Flatten the noise_data array for the texture
    noise_data_flat = noise_data.flatten()

    # Calculate expected size in bytes
    expected_size = size * size * size * 1 * 4  # 1 component, 4 bytes per float
    actual_size = noise_data_flat.nbytes  # Get the actual byte size

    print(f"Expected data size in bytes: {expected_size}")
    print(f"Actual data size in bytes: {actual_size}")

    # Ensure the actual size matches the expected size
    if actual_size != expected_size:
        raise ValueError(f"Data size mismatch: expected {expected_size}, got {actual_size}")

    # Create a 3D texture (size, size, size) with 1 component (grayscale)
    texture = ctx.texture3d((size, size, size), 4, noise_data_flat.tobytes())
    
    # Set texture filtering options
    texture.filter = (moderngl.LINEAR, moderngl.LINEAR)
    
    return texture, noise_data  # Return the raw noise data for saving

def save_noise_slice(noise_data, slice_index, filename):
    # Extract the slice from the 3D noise data
    slice_data = noise_data[:, :, slice_index]  # Get the desired slice

    # Normalize to [0, 255] for image saving
    slice_data_normalized = (slice_data * 255).astype(np.uint8)

    # Create a PIL image from the numpy array
    image = Image.fromarray(slice_data_normalized, mode='L')  # 'L' mode for grayscale

    # Save the image
    image.save(filename)
    print(f"Slice saved as {filename}")

# Create the 3D noise texture
size = 1000  # Size of the texture
scale = 0.1  # Scale for noise detail
texture3d, noise_data = create_noise_texture(ctx, size, scale)

# Save a slice of the noise texture
slice_index = 50  # Choose which slice to save
save_noise_slice(noise_data, slice_index, "lab/shader_tests/noise_slice.png")

# Main loop
clock = pygame.time.Clock()
while True:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Here you would typically render using the texture
    ctx.clear()
    # ctx.update(display, ui_surf, texture3d) # Assuming you have a method to handle rendering

    # Swap the buffers to display the result
    pygame.display.flip()
