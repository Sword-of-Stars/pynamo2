import moderngl
import numpy as np
from noise import snoise3

# Function to create a 3D texture using Perlin noise
def create_perlin_texture_3d(size, ctx, scale=1.0):
    """Generate a 3D texture using Perlin noise."""
    texture_data = np.zeros((size, size, size), dtype=np.float32)
    
    for z in range(size):
        for y in range(size):
            for x in range(size):
                # Generate Perlin noise value
                value = snoise3(x * scale, 
                                y * scale, 
                                z * scale, 
                                octaves=4, 
                                persistence=0.5, 
                                lacunarity=2.0)
                texture_data[x, y, z] = value
    
    # Normalize to [0, 1] range
    texture_data = (texture_data - texture_data.min()) / (texture_data.max() - texture_data.min())
    texture = ctx.texture3d((size, size, size), 3, texture_data.tobytes())

    return texture_data

# Main function
def main():
    # Create a ModernGL context
    ctx = moderngl.create_standalone_context()

    # Texture size
    size = 64  # Adjust size as needed

    # Create a Perlin noise 3D texture
    perlin_texture = create_perlin_texture_3d(size, ctx)

    # Generate the texture mipmaps (optional)
    perlin_texture.use()

    # If needed, you can save or use the texture in your rendering pipeline
    # For example, to write it to an image file, you could use OpenGL commands

if __name__ == "__main__":
    main()
