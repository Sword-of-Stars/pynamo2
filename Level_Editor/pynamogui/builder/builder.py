import pygame

from PIL import Image
from ..builder.autotiler import Autotiler

from ..builder.builder_functions import get_config, get_path_id, screen_to_chunk2
from ..misc.core_functions import screen_to_world, world_to_screen, get_images, prep_image, save_json

PATH_TO_SAVE = "maps"

# TODO: Clean up autotiler and export to an external configuration file for cleanliness

get_config(PATH_TO_SAVE)

class Builder():
    '''
    Handles map creation for the level editor from user input
    '''
    def __init__(self, gui):
        # the object the user has selected
        self.selected = None
        self.layer = 0
        self.z_order = 0

        self.database = {}
        self.current_map = {"name":"The Blight", "chunks":{"0;0":[]}} 
        self.current_map_path = "maps" # Save maps to this location/file

        self.gui = gui

        # save path, where are saved to
        self.path_to_save = PATH_TO_SAVE

        # Modes and Pseudofeatures #
        self.snap_to = True
        self.autotile = True
        self.show_grid = True
        self.show_trigger = True
        self.place_multiple = True
        self.can_scale = True # Bugged for now :%

        self.brush_size = 0

        self.just_clicked = False
        self.clicked = False

        self.load_database()

        self.autotiler = Autotiler()

        self.min_layer = -10
        self.max_layer = 10

    def set_regions(self):
        '''
        Extracts the header and world regions from the 'main' page

        NOTE: extremely bad coding, keep for now
        '''
        self.header = self.gui.pages['main'].regions[2]
        self.world = self.gui.pages['main'].regions[0]

        # we can't update the brush size until headers exist
        self.update_brush_size_header()

    def select(self, item):

        self.selected = item

        if item is not None:
            self.update_selected_header(self.selected.id)
        else:
            self.update_selected_header("None")

    def set_click(self, bool):
        self.clicked = bool

    def change_brush_size(self, delta):
        self.brush_size = max(0,int(self.brush_size+delta))
        self.update_brush_size_header()

        if self.selected != None:
            self.selected.set_size(self.brush_size)

    def place_asset(self, pos):
        self.world.place_asset(pos, self.layer, self.selected, 
                               self.current_map, snap_to=self.snap_to)
        
    def place_asset_by_coord(self, chunk, tile_pos):
        self.world.place_asset_by_coord(chunk, tile_pos, self.layer, self.selected.group, self.selected.id, 
                               self.current_map, snap_to=self.snap_to)
        
    def remove_asset(self, pos):
        # In later versions, condense this code from place asset
        tile_pos, chunk_id = self.world.get_tile_coord(pos)
        self.world.remove_asset(tile_pos, self.layer, chunk_id, self.current_map)

    def get_selected_chunk(self, pos):
        tile_pos, chunk_id = self.world.get_tile_coord(pos)

        if chunk_id not in self.current_map['chunks']:
            self.current_map['chunks'][chunk_id] = []

    def load_database(self):
        self.config = get_config(self.path_to_save)
        for key, item in self.config.items():
            try:
                with Image.open(item, "r") as img:
                    images = get_images(img)
                    for index, image in enumerate(images):
                        _id = f"ss;{key};{index}" # Currently, ss stands for spritesheet, may be deprecated later on
                        image = prep_image(image, 4) # Magic number
                        self.add_to_db(_id, image)

            except FileNotFoundError:
                print(f"[BUILDER] file {item} not found")

            except PermissionError:
                print(f"[BUILDER] permission to edit {item} denied")

    def add_to_db(self, _id, img):
        self.database[_id] = img

    def load_map(self, path): # Not certain how this fits together, but OK
        pass

    def save_map(self, path):
        # NOT USEd, reference config.functions
        save_json(path, self.current_map)
        print(f"[BUILDER] Saved map to {path}")
        
    def handle_button(self, event):
        if event.type == pygame.KEYDOWN:
            # update the layer
            if event.key == pygame.K_UP:
                self.update_layer(1)
            elif event.key == pygame.K_DOWN:
                self.update_layer(-1)

        # currently, due to sloppy coding, I handle triggers differently than 
        # normal text regions (thanks to typing)
        for _, region in self.gui.get_current_page().regions.items():
            if str(region) == "trigger":
                if region.visible:
                    region.handle_text(event)

    def update_layer(self, amt=1):
        self.layer += amt
        self.layer = max(min(self.max_layer, self.layer), self.min_layer) # bound the layer
        self.update_layer_text_header()

    def update_layer_text_header(self):
        self.header.modify_text('layer_num', self.layer)

    def update_selected_header(self, txt):
        self.header.modify_text('selected_txt', txt)

    def update_brush_size_header(self):
        self.header.modify_text('brush_size', self.brush_size)

    def update(self, pos, state, screen):
        if self.selected != None:
            self.selected.scale(self.world.scale)
            x, y = self.world.get_grid_coord(pos)

            # Set the position of the preview
            if self.snap_to:
                self.selected.rect.topleft = world_to_screen((x*self.world.SIZE, y*self.world.SIZE), 
                                                                self.world.offset, scale=self.world.scale)
            else:
                self.selected.rect.topleft = pos

            # Later, port to event
            if state[0] and self.world.is_over: # is the user hovering over the map?
                tiles = self.world.get_range_from_tile(pos, radius=self.brush_size)  

                if not self.autotile or not self.selected.autotilable: #band-aid soln for now
                    self.place_asset(pos)
                    for chunk, tile_pos in tiles:
                        self.place_asset_by_coord(chunk, tile_pos)

                elif self.autotile and self.selected.group == "tile":
                    for chunk, tile_pos in tiles:
                        self.handle_autotile(tile_pos, chunk)
        
            self.selected.update(screen)

        elif state[2]:
            tiles = self.world.get_range_from_tile(pos, radius=self.brush_size)
            for chunk, tile_pos in tiles: 
                self.remove(tile_pos, chunk)

        self.set_click(False)

    def update_autotiler(self, neighbors):
        for chunk_, tile_pos_, _ in neighbors:
            tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
            if tile != None and (tile["tile_ID"].split(";")[1] == self.selected.id.split(";")[1]): # check if in same spritesheet
                    self.autotiler.update(tile_pos_, chunk_, self, self.selected.id, self.selected.group)

    def handle_autotile(self, tile_pos, chunk_id):

        all_neighbors = self.world.get_neighbors(tile_pos, chunk_id)[2]
        
        self.place_asset_by_coord(chunk_id, tile_pos)

        self.autotiler.update(tile_pos, chunk_id, self, self.selected.id, self.selected.group)
        self.update_autotiler(all_neighbors)
        
    def remove_asset_autotile(self, pos):
        # In later versions, condense this code from place asset
        tile_pos, chunk_id = self.world.get_tile_coord(pos)
        tile_del = self.world.get_at(tile_pos, chunk_id, self.layer, self.current_map)

        if tile_del != None:

            id_ = tile_del["tile_ID"]
            group = tile_del["group"]

            self.world.remove_asset(tile_pos, self.layer, chunk_id, self.current_map)

            all_neighbors = self.world.get_neighbors(tile_pos, chunk_id)[2]

            for chunk_, tile_pos_, _ in all_neighbors:
                tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
                if tile != None and tile["auto?"]:
                    self.autotiler.update(tile_pos_, chunk_, self, id_, group)


    def remove(self, tile_pos, chunk_id):
       # In later versions, condense this code from place asset
        #tile_pos, chunk_id = self.world.get_tile_coord(pos)
        tile_del = self.world.get_at(tile_pos, chunk_id, self.layer, self.current_map)

        if tile_del != None:

            id_ = tile_del["tile_ID"]
            group = tile_del["group"]

            self.world.remove_asset(tile_pos, self.layer, chunk_id, self.current_map)

            if tile_del["auto?"]:

                all_neighbors = self.world.get_neighbors(tile_pos, chunk_id)[2]

                for chunk_, tile_pos_, _ in all_neighbors:
                    tile = self.world.get_at(tile_pos_, chunk_, self.layer, self.current_map)
                    if tile != None and tile["auto?"]:
                            self.autotiler.update(tile_pos_, chunk_, self, id_, group)


class BuilderUI():
    def __init__(self, builder):
        self.builder = builder

        self.buttons = []

    def add_button(self):
        pass
