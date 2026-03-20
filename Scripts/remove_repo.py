import sys
import json
from pathlib import Path

LOG_DIR = Path("./.crucible/logs")

def remove_package(name: str, silent: bool = False):
    """
    Remove all files listed under 'files' in the specified JSON log,
    then delete the JSON log itself. Folders are deleted only if empty.
    Confirmation required.

    :param name: Name of the log (without .json)
    """
    json_path = LOG_DIR / f"{name}.json"
    
    if not json_path.exists():
        print(f"No log found for '{name}'.")
        return

    # Load the JSON
    with json_path.open("r") as f:
        data = json.load(f)
    
    files_to_delete = data.get("files", [])
    Human_Name = data.get("name", "")
    Author = data.get("author", "")
    # Confirmation prompt
    if not silent:
        print(f"You are about to delete '{Human_Name}' by '{Author}'.")
        confirm = input("Continue? y/n  ")
        if confirm.lower() == "n":
            sys.exit("Exiting...")

    # Delete each path
    for file_path in files_to_delete:
        path_obj = Path(file_path)
        try:
            if path_obj.is_file():
                path_obj.unlink()
                print(f"Deleted file: {file_path}")
            elif path_obj.is_dir():
                if not any(path_obj.iterdir()):  # folder is empty
                    path_obj.rmdir()
                    print(f"Deleted empty folder: {file_path}")
                else:
                    print(f"Skipped non-empty folder: {file_path}")
            else:
                print(f"Skipped missing path: {file_path}")
        except Exception as e:
            print(f"Error deleting {file_path}: {e}")

    # Delete the JSON log itself
    try:
        json_path.unlink()
        print(f"Deleted log: {json_path}")
    except Exception as e:
        print(f"Error deleting log: {e}")