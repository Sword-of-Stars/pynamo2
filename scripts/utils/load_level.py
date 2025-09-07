from scripts.utils.file_io import load_json
from scripts.rendering.camera import world_to_screen
from scripts.entities.obstacle import Obstacle, TileObstacle
from scripts.entities.trigger import Trigger
from scripts.tiles.tilemap import Tilemap

from collections import defaultdict

def load_level(filename):
    data = load_json(filename)

    loaded_level = {}

    for key, item in data.items():
        if key == "obstacles": # load all obstacles into scene

            loaded_level["obstacles"] = []
            for obstacle in item:

                rect = obstacle["rect"]
                color = obstacle["color"]

                loaded_level["obstacles"].append(Obstacle(rect=rect, color=color))
    Tilemap()
    
    return loaded_level

            
def load_level_updated(filename, tilemap, trigger_path="data/configs/triggers.json"):
    '''
    This only serves to extract the necessary data for use in the rendering
    system, doesn't need to actually calculate the correct position of the tile

    Or maybe it can, to save compuational time? IDK...
    '''
    data = load_json(filename)
    triggers = load_json(trigger_path)

    loaded_level = {"obstacles": defaultdict(list),
                    "triggers":[]}

    # Get the current map chunks from the builder
    chunks = data['chunks']

    # Define some constants for magic numbers to improve readability
    TILE_SIZE = 64
    CHUNK_SIZE = 4

    # Build level from chunks
    for chunk, contents in chunks.items():
        # Convert chunk key to chunk coordinates
        cx, cy = map(int, chunk.split(";"))

        for item in contents:
            # find the tile's location within the chunk
            x, y = item["pos"] 

            # Compute the world position of the tile
            tile_pos = ((x + cx * CHUNK_SIZE) * TILE_SIZE, (y + cy * CHUNK_SIZE) * TILE_SIZE)
            pos = world_to_screen(tile_pos, (0,0), 1)

            # Apply the tile's offset to the position
            pos = [p + item['offset'][i] for i, p in enumerate(pos)]           

            if item["group"] == "tile":
                img = tilemap.db[item["tile_ID"]]

                # probs rename neighbors
                loaded_level["obstacles"][chunk].append(TileObstacle(pos=pos, rect=(*pos, TILE_SIZE, TILE_SIZE), 
                                                              layer=item["z-order"], img=img))
                
            elif item["group"] == "trigger":

                # potentially, assign triggers colors for easier debugging
                color = (255,100,100)
                if "color" in item:
                    color = item["color"]

                config = triggers[item["tile_ID"]]
                    
                loaded_level["triggers"].append(Trigger(layer=item["z-order"], _id=item["tile_ID"], config=config,
                                                        pos=pos, rect=(*pos, TILE_SIZE, TILE_SIZE), color=color))

    return loaded_level

'''
"""
      Draws the current world with all its tiles, decor, and triggers on the screen.

      This method calculates which chunks are visible on the screen, gathers all the 
      tiles from those chunks, and sorts them by z-order for correct rendering.

      Parameters:
      -----------
      screen : pygame.Surface
         The surface to render the world on.
      """

      # Get the current map chunks from the builder
      chunks = self.builder.current_map['chunks']

      # Define some constants for magic numbers to improve readability
      TILE_SIZE = 64
      CHUNK_SIZE = 4

      # List to store all the tiles and their z-order for rendering
      renderer = []

      # Determine the visible area of the screen in terms of chunks
      ax, ay = screen_to_chunk(self.rect.topleft, self.offset, scale=self.scale)
      bx, by = screen_to_chunk(self.rect.bottomright, self.offset, scale=self.scale)

      # Calculate the number of chunks to check (with a buffer)
      c_dx = bx - ax + 1
      c_dy = by - ay + 1

      # Generate the list of visible chunk keys
      visible_chunks = [f"{ax+x};{ay+y}" for x in range(-1, c_dx) for y in range(-1, c_dy)]

      # Loop through each chunk in the world
      for key, chunk in chunks.items():
         if key not in visible_chunks:
            continue

         # Convert chunk key to chunk coordinates
         cx, cy = map(int, key.split(";"))

         # Iterate through each tile in the chunk
         for tile in chunk:
            x, y = tile['pos']

            # Compute the world position of the tile
            tile_pos = ((x + cx * CHUNK_SIZE) * TILE_SIZE, (y + cy * CHUNK_SIZE) * TILE_SIZE)
            pos = world_to_screen(tile_pos, self.offset, self.scale)

            # Apply the tile's offset to the position
            pos = [p + tile['offset'][i] * self.scale for i, p in enumerate(pos)]

            # Load the tile image and scale it based on the current zoom level
            if tile['group'] == "trigger":
               img = pygame.transform.scale_by(self.builder.database["trigger"], self.scale)
            else:
               img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)

            # Sort tiles by z-order (higher values drawn last) and by vertical position
            renderer.append((img, pos, tile["z-order"]))

            # Special case for decor tiles (similar logic for now but can be extended later)
            if tile['group'] == 'decor':
                renderer.append((img, pos, tile["z-order"]))

            # Render trigger tiles if they should be shown
            if tile['group'] == 'trigger' and self.builder.show_trigger:
                trigger_img = pygame.transform.scale_by(self.trigger, self.scale)
                renderer.append((trigger_img, pos, tile["z-order"]))

      # Render the tiles, sorting by z-order and Y position for proper layering
      for img, pos, _ in sorted(renderer, key=lambda x: (x[2], x[1][1])):  # Sort by z-order and vertical position
         screen.blit(img, pos)
'''