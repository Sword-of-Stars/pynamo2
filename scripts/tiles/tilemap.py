from scripts.utils.file_io import load_json, get_images, prep_image
from PIL import Image

class Tilemap():
    '''
    Creates a database of all images, tiles and assets used
    '''
    def __init__(self):
        self.config_path = "data/configs/tilesets.json"
        self.db = {}
        self.load_db()

    def load_db(self):
        self.config = load_json(self.config_path)
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
        self.db[_id] = img