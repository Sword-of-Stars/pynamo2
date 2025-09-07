import pygame

from ...gui_elements.region import Region

from ...misc.core_functions import world_to_screen, screen_to_world, screen_to_chunk

class WorldBox(Region):
   def __init__(self, config):
      Region.__init__(self, *config['rect'], body_color=(0,0,0), border_color=(0,0,0))

      self.offset = [-x for x in self.rect.center]
      self.original_offset = self.offset.copy()

      self.chunk_size = 4

      self.scale = 1
      self.pre_scale = 1
      self.scroll_speed = 0.1 # how quickly the screen scales
      self.scroll_min = 0.125
      self.scroll_max = 4

      self.dimensions = [1000, 1000, 1000, 1000]
      self.SIZE = config['size']
      self.is_over = False

      self.grid_color = (200, 100, 100)

      self.load_trigger_surface()

   def draw_grid(self, screen):
      '''
      Draws an overlay grid over the level space, centered at (0, 0).
      '''

      def draw_line(start, end, width):
         '''
         Helper function to draw a line with bounds checking.
         Ensures that lines stay within the defined rect.
         '''
         # Ensure the line's start and end points stay within the defined area (self.rect)
         start[0] = max(self.rect.left, start[0])
         start[1] = max(self.rect.top, start[1])
         end[0] = min(self.rect.right, end[0])
         end[1] = min(self.rect.bottom, end[1])

         pygame.draw.line(screen, self.grid_color, start, end, width=width)

      l, r, u, d = self.dimensions
      world_origin = world_to_screen((0, 0), self.offset, self.scale)

      # Draw vertical grid lines
      for i in range(-l, r + 1):
         top = world_to_screen((i * self.SIZE, -u * self.SIZE), self.offset, self.scale)
         
         # If the line is out of bounds, exit early to optimize
         if top[0] > self.rect.right:
            break
         if top[0] >= self.rect.left:
            bottom = world_to_screen((i * self.SIZE, d * self.SIZE), self.offset, self.scale)
            width = 5 if i == 0 else 1  # Draw thicker line at origin (i=0)
            draw_line(top, bottom, width)

      # Draw horizontal grid lines
      for i in range(-u, d + 1):
         left = world_to_screen((-l * self.SIZE, i * self.SIZE), self.offset, self.scale)
         
         # If the line is out of bounds, exit early to optimize
         if left[1] > self.rect.bottom:
            break
         if left[1] >= self.rect.top:
            right = world_to_screen((r * self.SIZE, i * self.SIZE), self.offset, self.scale)
            width = 5 if i == 0 else 1  # Draw thicker line at origin (i=0)
            draw_line(left, right, width)

      # Draw a circle at the origin if it's within the visible area
      if self.rect.collidepoint(world_origin):
         pygame.draw.circle(screen, self.grid_color, world_origin, 10)

   def pan(self, pos, rel):
      '''
      Pan the screen in accordance with user input
      '''
      # if the user's mouse is over the world and not holding
      # an object to place, pan the screen
      if self.rect.collidepoint(pos) and self.builder.selected == None:
         self.offset[0] -= rel[0]/self.scale
         self.offset[1] -= rel[1]/self.scale

   def scroll_event(self, event, pos):
      '''
      Handles scrolling events (zooming in and out)
      '''
      if self.rect.collidepoint(pos) and self.builder.can_scale:
         self.pre_scale = max(min(self.scale+event.y*self.scroll_speed, self.scroll_max), self.scroll_min)

   def get_grid_coord(self, pos):
      x, y = screen_to_world(pos, self.offset, scale=self.scale)
      return (int(x//self.SIZE),int(y//self.SIZE))
   
   def get_chunk_from_grid(self, tile_pos):
      x, y = tile_pos
      chunk_id = f"{int(x//4)};{int(y//4)}"
      return chunk_id

   def get_screen_coord(self, world_coords):
      return world_to_screen(world_coords, self.offset, scale=self.scale)
   
   def get_tile_coord(self, pos):
      # cx, cy describes the x- and y-coordinate of the active chunk
      cx, cy = screen_to_chunk(pos, self.offset, self.scale)

      # px, py decribes the coordinate of the square within the chunk
      px, py = self.get_grid_coord(pos)
      tile_pos = [int(px%4), int(py%4)]
      chunk_id = f"{cx};{cy}"

      return tile_pos, chunk_id

   def calculate_offset(self, state, pos, rel):
      if state[0]: # and the builder has nothing selected
         self.pan(pos, rel)

      world_before_zoom = screen_to_world(pos, self.offset, self.scale)
      self.scale = self.pre_scale
      world_after_zoom = screen_to_world(pos, self.offset, self.scale)

      self.offset[0] += world_before_zoom[0] - world_after_zoom[0]
      self.offset[1] += world_before_zoom[1] - world_after_zoom[1]

   def set_grid(self, val):
      self.show_grid = val

   def load_trigger_surface(self):
      size = 64
      self.trigger = pygame.Surface((size,size))
      pygame.draw.rect(self.trigger, (20,240,120), (0,0,size,size))

   def draw_world(self, screen):
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
            # these lines are exactly the same, wtf
            #if tile['group'] == "trigger":
            img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)
            #else:
            #img = pygame.transform.scale_by(self.builder.database[tile['tile_ID']], self.scale)

            # Sort tiles by z-order (higher values drawn later) and by vertical position
            renderer.append((img, pos, tile["z-order"]))

            # Special case for decor tiles (similar logic for now but can be extended later)
            if tile['group'] == 'decor':
                renderer.append((img, pos, tile["z-order"]))

            # Render trigger tiles if they should be shown
            #if tile['group'] == 'trigger' and self.builder.show_trigger:
                #trigger_img = pygame.transform.scale_by(self.trigger, self.scale)
                #renderer.append((trigger_img, pos, tile["z-order"]))

      # Render the tiles, sorting by z-order and Y position for proper layering
      for img, pos, _ in sorted(renderer, key=lambda x: (x[2], x[1][1])):  # Sort by z-order and vertical position
         screen.blit(img, pos)

   def place_asset(self, pos, layer, selected, current_map, snap_to=False):
      """
      Places an asset (tile or object) onto the current map based on the given position, layer, and selection.

      Parameters:
      -----------
      pos : tuple
         The (x, y) screen coordinates where the asset is to be placed.
      
      layer : int
         The z-order layer where the asset should be placed. Higher layers are drawn on top of lower layers.
      
      selected : object
         The currently selected asset (tile or object) that will be placed on the map. 
         This object must contain `id`, `group`, and `autotilable` attributes.
      
      current_map : dict
         The map data that contains information about all the chunks and tiles on the current map.
      
      snap_to : bool, optional
         Whether the asset should snap to the grid or be placed freely (default is False).

      Process:
      --------
      1. Converts the given screen position `pos` into chunk coordinates (`cx`, `cy`), which represent 
         the active chunk on the map where the asset will be placed.
      2. Calculates the position of the asset within the chunk (`px`, `py`) using a grid system.
         If snap-to-grid is enabled, the coordinates are rounded to fit the grid.
      3. If `snap_to` is False, the asset is placed freely at the exact world position (`mx`, `my`) instead 
         of snapping to the grid.
      4. Creates a new object dictionary (`new_obj`) representing the asset and its properties, including
         tile ID, group, z-order, position within the chunk, and offsets for freeform placement.
      5. Removes any existing asset in the same position and layer to ensure the new asset replaces it.
      6. Appends the new object to the corresponding chunk in the `current_map`.

      Notes:
      ------
      - This method handles both grid-snapped and freeform placement.
      - It optimizes the placement of assets by removing the existing ones in the same location and layer.
      """

      # Convert screen coordinates to chunk coordinates (cx, cy)
      cx, cy = screen_to_chunk(pos, self.offset, self.scale)

      # Get the position within the chunk (px, py), snapped to a grid of 4x4 tiles
      px, py = self.get_grid_coord(pos)
      px = int(px % 4)  # Modulus to ensure the position stays within the chunk's grid
      py = int(py % 4)

      # Freeform placement if not snapped to grid
      mx, my = 0, 0
      if not snap_to:
         mx, my = screen_to_world(pos, self.offset, scale=self.scale)
         mx, my = int(mx), int(my)

      # Create a new object dictionary representing the asset to place on the map
      new_obj = {
         "tile_ID": selected.id,  # The ID of the selected tile or object
         "group": selected.group,  # Group (e.g., 'tile', 'decor', 'trigger') to which the asset belongs
         "z-order": layer,  # Z-order layer to control rendering order
         "pos": [px, py],  # Position within the chunk grid
         "offset": [mx, my],  # Offset for freeform placement (only used if snap_to=False)
         "sum": 0,  # Additional data for future use (can be calculated later)
         "auto?": int(selected.autotilable)  # Indicates whether the tile is autotilable (0 or 1)
      }

      # Get the unique chunk ID based on chunk coordinates
      chunk_id = f"{cx};{cy}"

      # Clear the map for new asset
      self.remove_asset(new_obj['pos'], new_obj['z-order'], chunk_id, current_map)

      current_map['chunks'][chunk_id].append(new_obj)

   def place_asset_by_coord(self, chunk_id, tile_pos, layer, group, id_, current_map, snap_to=False, offset=[0,0], auto=False, neighbors=[]):

      # Create and place new object reference - doesn't need to be over-optimized
      new_obj = {"tile_ID":id_, "group":group,
                  "z-order":layer,"pos":tile_pos, "offset":[x*self.chunk_size for x in offset],
                  "sum":0,"auto?":int(auto), "neighbors":neighbors}
      
      # Clear the map for new asset
      self.remove_asset(new_obj['pos'], new_obj['z-order'], chunk_id, current_map)

      current_map['chunks'][chunk_id].append(new_obj)

   def remove_asset(self, obj_pos, obj_layer, chunk_id, current_map):
      if chunk_id not in current_map['chunks']:
         current_map['chunks'][chunk_id] = []

      for i in current_map['chunks'][chunk_id]:
         if i["pos"] == obj_pos and i['z-order'] == obj_layer:
               current_map['chunks'][chunk_id].remove(i)
               break      

   def get_at(self, tile_pos, chunk_id, layer, current_map):
      if chunk_id in current_map['chunks']:
         chunk = current_map['chunks'][chunk_id]
         for tile in chunk:
            if tile['pos'] == tile_pos and tile['z-order'] == layer:
               return tile
      return None
      
   def get_neighbors(self, tile_pos, chunk_id):

      def concat_chunk(x, y):
         return f"{x};{y}"
      # chunk_id is given as the hash key in the form "1;2"
      # tile is given as [0,3]
      # given neighbors in the form of a dictionary
      # i.e. {"1;2":[0,3], "2;2"[0,1]}]
      cardinal_neighbors = []
      diagonal_neighbors = []
      cx, cy = [int(c) for c in chunk_id.split(";")]
      x, y = tile_pos

      # Compute surrounding chunks
      up_chunk = f"{cy - (not y)}"
      down_chunk = f"{cy + y // (self.chunk_size - 1)}"
      right_chunk = f"{cx + x // (self.chunk_size - 1)}"
      left_chunk = f"{cx - (not x)}"

      # Compute neighbor tile positions
      lx, rx = (x - 1) % self.chunk_size, (x + 1) % self.chunk_size
      uy, dy = (y - 1) % self.chunk_size, (y + 1) % self.chunk_size

      # Direction mappings for cardinal and diagonal neighbors
      directions = {
         "cardinal": [
            ("up", (cx, up_chunk, x, uy)),
            ("right", (right_chunk, cy, rx, y)),
            ("down", (cx, down_chunk, x, dy)),
            ("left", (left_chunk, cy, lx, y))
         ],
         "diagonal": [
            ("up-right", (right_chunk, up_chunk, rx, uy)),
            ("down-right", (right_chunk, down_chunk, rx, dy)),
            ("up-left", (left_chunk, up_chunk, lx, uy)),
            ("down-left", (left_chunk, down_chunk, lx, dy))
         ]
      }

      # Generate neighbors
      cardinal_neighbors = [
         [concat_chunk(chunk_x, chunk_y), [tile_x, tile_y], direction]
         for direction, (chunk_x, chunk_y, tile_x, tile_y) in directions["cardinal"]
      ]

      diagonal_neighbors = [
         [concat_chunk(chunk_x, chunk_y), [tile_x, tile_y], direction]
         for direction, (chunk_x, chunk_y, tile_x, tile_y) in directions["diagonal"]
      ]

      all_neighbors = []
      all_neighbors.extend(cardinal_neighbors)
      all_neighbors.extend(diagonal_neighbors)

      return cardinal_neighbors, diagonal_neighbors, all_neighbors

   def get_range(self, pos1, pos2):
      p1 = self.get_grid_coord(pos1)
      p2 = self.get_grid_coord(pos2)

      topleft = [int(min(p1[0], p2[0])), int(max(p1[1], p2[1]))]
      botright = [int(max(p1[0], p2[0])), int(min(p1[1], p2[1]))]

      return topleft, botright
   
   def get_range_from_tile(self, pos, radius=4):
      wx, wy = screen_to_world(pos, self.offset, self.scale)

      tx, ty = int(wx//64), int(wy//64)
      
      tiles = []
      for x in range(tx-radius, tx+radius + 1):
         for y in range(ty-radius, ty+radius+1):
            tile_pos = [self.get_chunk_from_grid((x,y)),[x%4,y%4]]
            tiles.append(tile_pos)

      return tiles

   def get_tiles_in_range(self, tl, br):
      c1 = self.get_chunk_from_grid(tl)
      c2 = self.get_chunk_from_grid(br)

   def update(self, pos, state, rel, screen):
      if self.visible:
         self.draw(screen)
         self.calculate_offset(state, pos, rel)

         self.is_over = self.rect.collidepoint(pos)

         self.draw_world(screen)

         if self.builder.show_grid:
            self.draw_grid(screen)
