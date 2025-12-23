import pygame

from scripts.utils.file_io import load_json
from scripts.rendering.animations import extract_spritesheet


class AssetManager:
    '''
    This class initializes and stores all entities, setting their 
    class methods appropriately, using @classmethod
    '''
    _assets = {}
    
    @staticmethod
    def load_asset(name, category, data=[]):
        '''
        Loads an asset
        
        This makes sure loading operations 
        only ever happen one time
        '''
        if name not in AssetManager._assets:
            if category == "sfx":
                AssetManager._assets[name] = pygame.mixer.music.load(f"/data/sfx/{name}")
            elif category == "spritesheet":
                AssetManager._assets[name] = extract_spritesheet(*data)
            else:
                print(f"[ASSET MANAGER] {category} is not a supported data type")
                return
        return AssetManager._assets[name]

    @staticmethod
    def get_asset(key):
        if key in AssetManager._assets:
            return AssetManager._assets[key]
        return None