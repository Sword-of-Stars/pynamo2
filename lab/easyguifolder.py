import os
import easygui
from PIL import Image

def navigate_directory():
    # Start with the current directory
    current_dir = os.getcwd()
    
    while True:
        # List all files and directories in the current directory
        items = os.listdir(current_dir)
        
        # Add an option to go up one level
        if current_dir != os.path.abspath(os.sep):
            items.insert(0, ".. (Up one level)")
        
        # Show the list of items in a choice box
        choice = easygui.choicebox(f"Current Directory: {current_dir}", "Directory Navigation", items)
        
        if not choice:
            # If the user cancels, exit the loop
            break
        
        if choice == ".. (Up one level)":
            # Go up one level
            current_dir = os.path.dirname(current_dir)
        else:
            # Get the full path of the selected item
            selected_path = os.path.join(current_dir, choice)
            
            if os.path.isdir(selected_path):
                # If it's a directory, navigate into it
                current_dir = selected_path
            else:
                # If it's a file, check if it's an image
                if selected_path.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                    # Display the image
                    img = Image.open(selected_path)
                    img.show()
                else:
                    # If it's not an image, show its content as text
                    with open(selected_path, 'r') as file:
                        content = file.read()
                        easygui.textbox(f"Content of {choice}", "File Content", content)

# Run the directory navigation system
navigate_directory()