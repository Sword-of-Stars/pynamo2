import easygui, os

# Open a file dialog that only shows .json files
file_path = easygui.fileopenbox(msg="Select a JSON file", default=f"{os.getcwd()}/*.json", filetypes=["*.json"])

if file_path:
    print(f"Selected file: {file_path}")
else:
    print("No file selected.")