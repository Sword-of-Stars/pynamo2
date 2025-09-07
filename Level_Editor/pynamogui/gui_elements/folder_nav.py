import os
import easygui

def save_file(default=""):
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
     
    return f"{output_directory}/{file_name}"


def exit_gui():
    return "Yes" == easygui.buttonbox(msg=f"Save before exiting?", 
                                        choices=["Yes", "No"])
        

