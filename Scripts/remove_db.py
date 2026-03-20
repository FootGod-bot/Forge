from pathlib import Path
import os
import json


script_dir = Path(__file__).resolve().parent

def remove_db(name, silent: bool = False):
    file = name + ".json"
    db_dir = os.path.join(script_dir, "databases")
    db = os.path.join(db_dir, file)
    
    
    with file.open("r") as f:
        data = json.load(f)
    name = data.get("Name", "")
    author = data.get("Author", "")
    if not silent:
        print(f"You are about to delete {name} by {author}")
        confirm = input("Continue? y/n  ")
        if confirm.lower() == "y":
            os.remove(db)
    
    
if __name__ == "__main__":
    remove_db("test")