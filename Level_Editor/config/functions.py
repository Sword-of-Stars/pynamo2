import os
import json
import easygui

from pynamogui.misc.core_functions import save_json

def change_page(gui, page):
    gui.current_page = page
    
def change_visible_regions(gui, off, on):
    current_page = gui.pages[gui.current_page]
    for region in off: 
        current_page.regions[region].visible = False
    for region in on: 
        current_page.regions[region].visible = True

def change_palette(gui, config):
    gui.builder.palette.get_images(config)

def save_file(map_data, path):
    #name = input("Name your file: ") # Make a UI feature later
    name = "xandaria"
    with open(f"maps/{name}.json", "w") as json_file:
        json.dump(map_data, json_file, ensure_ascii=False) #, indent=4
    
def load_file(builder, path="../RPG_Base/maps"):

    try:
        file_path = easygui.fileopenbox(msg="Select a JSON file", default=f"{os.getcwd()}/*.json", filetypes=["*.json"])
        with open(file_path, "r") as load_file:
            file = json.load(load_file)
            
    except:
        print(f"There was an error reading the file")

    try:
        builder.current_map = file
    except:
        print("Uh, boss? Something went wrong ...")

def new_map(size):
    # In the future, perhaps include additional data, such as the map name, 
    # or other important ID info
    map_data = {"SIZE":size, "map_data":{}}
    print("<NEW MAP>")
    return map_data

def go_to_settings():
    print("Moving, sarge!")

def save_file(current_map, default=""):
    # default name (perhaps load from legacy for convenience?)
    # default save location is the cwd
    cwd = os.getcwd()

    # get the output folder
    output_directory = easygui.diropenbox(msg="Select output directory", default=cwd)
    existing_files = os.listdir(output_directory)

    # set the name of the save file
    while True:
        file_name = easygui.enterbox(msg="Enter the name of the file to be saved (no extension needed):", default=default)
        if f"{file_name}.json" in existing_files:
            overwrite = easygui.buttonbox(msg=f"File with name '{file_name}.json' already exists. \nOverwrite?", 
                                        choices=["Yes", "No"])
            if overwrite == "No":
                continue
        break

    # save the current map to the specified folder
    save_json(f"{output_directory}/{file_name}", current_map)
