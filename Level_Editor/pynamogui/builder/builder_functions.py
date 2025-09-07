import os
import json

from ..misc.debugging_utils import find_caller

def load_json(path):
    with open(path, "r") as load_file:
        file = json.load(load_file)
    return file

def get_config(folder_path):
    """
    Loads a configuration file (`config.json`) from the specified folder path. 
    If the file does not exist, it creates an empty configuration file.

    Parameters:
    -----------
    folder_path : str
        The path to the folder where the configuration file (`config.json`) is or should be located.

    Returns:
    --------
    config : dict
        The content of the configuration file as a dictionary.
        If the file does not exist, an empty dictionary is returned after creating the file.

    Behavior:
    ---------
    1. Constructs the full file path to `config.json` within the specified `folder_path`.
    2. Checks if the `config.json` file exists at the constructed path:
       - If it exists, loads the JSON content from the file.
       - If it does not exist, creates an empty JSON file (`{}`) and writes it to disk.
    3. Returns the loaded JSON content as a Python dictionary.

    Example:
    --------
    folder_path = "/my/folder"
    
    If `config.json` exists:
    >>> get_config(folder_path)
    {"1": "/path/to/file1", "2": "/path/to/file2"}

    If `config.json` does not exist:
    >>> get_config(folder_path)
    {}  # Empty dictionary, and a new config.json file is created
    """

    file_path = os.path.join(folder_path, 'config.json')  # Construct the file path

    if not os.path.exists(file_path):
        json_data = json.dumps({})
        
        with open(file_path, 'w') as json_file:
            json_file.write(json_data)

    return load_json(file_path)

def get_path_id(config_path, path):
    """
    Retrieve the ID (key) corresponding to a given file path from a JSON file.
    If the path does not exist in the JSON, a new key is generated, stored, and returned.

    Parameters:
    -----------
    config_path : str
        The path to the JSON configuration file containing key-value pairs.
    path : str
        The file path to search for or add in the JSON.

    Returns:
    --------
    key : int
        The key (ID) associated with the provided path. If the path does not exist, a new key is created.

    Behavior:
    ---------
    1. Loads the JSON file from `config_path`.
    2. Checks if the specified `path` exists in the JSON file:
       - If it exists, return its associated key.
       - If it does not exist, a new key is generated, assigned to the path, and added to the JSON.
    3. Saves the updated JSON back to the file, overwriting the original.
    4. Returns the key corresponding to the file path.
    
    Notes:
    ------
    - The keys in the JSON file are assumed to be integers.
    - If no keys exist in the file, the function assigns the first key as 0.
    
    Example:
    --------
    config.json:
    {
        "1": "/path/to/file1",
        "2": "/path/to/file2"
    }
    
    >>> get_path_id("config.json", "/path/to/file3")
    3  # New key created
    
    >>> get_path_id("config.json", "/path/to/file1")
    1  # Existing key returned
    """

    # Load JSON data from file
    json_data = load_json(config_path)

    # Find if the path exists in the current JSON data
    for key, item in json_data.items():
        if item == path:
            break

    else:
        # If no key is found, find the largest existing key
        largest_key = max(map(int, json_data.keys())) if json_data.keys() else -1
        
        # Create a new key-value pair
        new_key = str(largest_key + 1)
        json_data[new_key] = path
        
        key = new_key

    # Convert the dictionary back to a JSON string
    json_string = json.dumps(json_data, indent=4)  # Added indent for better readability


    # Overwrite the JSON file with the updated content
    with open(config_path, "w") as json_file:
        json_file.write(json_string)

    return key

def get_images_from_db(db, path_id):
    images = []
    for key, item in db.items():
        try:
            if path_id == key.split(";")[1]:
                images.append(item)
        except IndexError:
            pass # let error pass silently :^(
    return images
      
def generate_id(type, path, index, config_path):
    if type == 'spritesheet':
        method = 'ss'
    else:
        method = 'xx'
    
    return f"{method};{get_path_id(config_path, path)};{index}"

def read_id(ID, config_path):
    method, path, index = ID.split(".") # ex. ss.000.002

def save_json(data, path):
    print(f"writing to {path}")
    json_string = json.dumps(data)
    with open(f"{path}.json", "w") as json_file:
        json_file.write(json_string)

#-- Non-universalized World Transforms --#
CHUNK_DIVISOR = 4
SIZE = 64

def screen_to_world(screen_coords, offset, SIZE=SIZE, scale=1):
    screen_x, screen_y = screen_coords
    offset_x, offset_y = offset
    world_x = (screen_x/scale) + offset_x
    world_y = (screen_y/scale) + offset_y
    return [int(world_x//SIZE), int(world_y//SIZE)]

def get_chunk_id2(pos):
    x, y = pos
    #divisor = CHUNK_SIZE/SIZE
    divisor = CHUNK_DIVISOR
    return (x//divisor, y//divisor)

def screen_to_chunk2(pos, offset, scale=1):
    return get_chunk_id2(screen_to_world(pos, offset, scale=scale))

