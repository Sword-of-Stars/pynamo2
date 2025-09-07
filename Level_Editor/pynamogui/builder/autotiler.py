import pygame, sys

class Autotiler:
    def __init__(self):
        self.cardinal = {
                "up": 1,
                "right": 2,
                "down": 4,
                "left": 8
                }
            
        self.diagonal = {
            "up-left": 16,
            "up-right": 32,
            "down-left": 64,
            "down-right": 128,
            }

        self.autotile_conversion = {
            6:0, 7:1, 3:23, 35:2, 12:3, 15:27, 11:27, 12:6, 13:17, 9:20, 25:8,
            2:9, 140:11, 0:15,  5: 21, 1:24, 4:18, 134:0, 135:17, 76:6,
            78:3, 10:3, 14:3, 142:3, 59:5, 206:3, 255:4, 167:1,93:7, 207:27,
            8:12, 175:14, 63:4, 191:13, 77:20, 29:7, 39:1, 27:17, 159:11, 223:11,
            43:14, 47:20, 111:14, 95:17,
            31:17,79:27,239:14, 
            127:10,143:27}

        self.offsets = {}

    def update(self, tile_pos, chunk, builder, id, group):
        cardinal_neighbors, diagonal_neighbors = builder.world.get_neighbors(tile_pos, chunk)[:2]
        cardinal_directions = []#["left","right","up","down"]

        bitmap_sum = 0

        # go thorough all of a tile's neighbors
        for chunk_, tile_pos_, direction in cardinal_neighbors:
            tile = builder.world.get_at(tile_pos_, chunk_, builder.layer, builder.current_map)
            if tile != None:
                if tile["tile_ID"].split(";")[1] == id.split(";")[1]:
                    bitmap_sum += self.cardinal[direction]
                else:
                    for diag_tile in reversed(diagonal_neighbors):
                        if direction in diag_tile[2]:
                            diagonal_neighbors.remove(diag_tile)
            else:
                cardinal_directions.append(direction)
                for diag_tile in reversed(diagonal_neighbors):
                    if direction in diag_tile[2]:
                        diagonal_neighbors.remove(diag_tile)

        for chunk_, tile_pos_, direction in diagonal_neighbors:
            tile = builder.world.get_at(tile_pos_, chunk_, builder.layer, builder.current_map)
            if tile != None:
                if tile["tile_ID"].split(";")[1] == id.split(";")[1]:
                    bitmap_sum += self.diagonal[direction]

        tile_index = self.autotile_conversion[bitmap_sum]
        spritesheet, index, _ = id.split(";")

        #self.selected.img = self.database[f"{spritesheet};{index};{self.layer+10}"]

        offset = 0
        if tile_index in self.offsets:
            offset = self.offsets[tile_index]

        #print(f"[AUTOTILER] cardinal neighbors: {cardinal_neighbors}")
        #print(bitmap_sum)
        
        builder.world.place_asset_by_coord(chunk, tile_pos, builder.layer, group, 
                                        f"{spritesheet};{index};{tile_index}", builder.current_map, offset=[offset,0], auto=True,
                                        neighbors=cardinal_directions)

        return tile_index