import easygui
import os

def create_directory(path):
    if not os.path.exists(path):
        os.makedirs(path)

def main():
    # Prompt user to select a default output folder
    default_output_folder = easygui.diropenbox(msg="Select the output folder")

    if not default_output_folder:
        easygui.msgbox("No folder selected. Exiting...")
        return

    # Prompt user to create a new folder within the default output folder
    new_folder_name = easygui.enterbox(msg="Enter the name of the new folder (leave blank to skip):")

    if new_folder_name:
        new_folder_path = os.path.join(default_output_folder, new_folder_name)
        create_directory(new_folder_path)
    else:
        new_folder_path = default_output_folder

    # Prompt user to enter the name of the file to be saved
    file_name = easygui.enterbox(msg="Enter the name of the file to be saved (with extension):")

    if not file_name:
        easygui.msgbox("No file name entered. Exiting...")
        return

    # Create the full file path
    file_path = os.path.join(new_folder_path, file_name)

    # Save an empty file at the specified location
    with open(file_path, 'w') as f:
        f.write("")

    easygui.msgbox(f"File '{file_name}' has been created at '{new_folder_path}'.")

if __name__ == "__main__":
    main()