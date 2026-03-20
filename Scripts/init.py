import subprocess
import os
import shutil
import json
import sys

if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a normal Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
currentwrkdir = os.getcwd()
datafolder = os.path.join(script_dir, "databases")
JsonData = {
  "name": "Project",
  "tree": {
    "$className": "DataModel",

    "ReplicatedStorage": {
      "$path": "src/ReplicatedStorage"
    },

    "ServerScriptService": {
      "$path": "src/ServerScriptService"
    },

    "ServerStorage": {
      "$path": "src/ServerStorage"
    },

    "StarterPlayer": {
      "StarterPlayerScripts": {
        "$path": "src/StarterPlayer/StarterPlayerScripts"
      },
      "StarterCharacterScripts": {
        "$path": "src/StarterPlayer/StarterCharacterScripts"
      }
    },

    "StarterGui": {
      "$path": "src/StarterGui"
    },

    "StarterPack": {
      "$path": "src/StarterPack"
    },

    "SoundService": {
      "$path": "src/SoundService"
    },

    "Lighting": {
      "$path": "src/Lighting"
    },

    "TextChatService": {
      "$path": "src/TextChatService"
    },

    "Teams": {
      "$path": "src/Teams"
    }
  }
}

def init(silent):
    print("Initializing...")
    if not os.path.exists(datafolder):
        os.mkdir(datafolder)
    
    
    printIt = False
    filesToDel = ["default.project.json", ".gitignore", "README.md"]
    foldersToDel = ["src"]
    if os.path.exists(os.path.join(currentwrkdir, "default.project.json")):
        printIt = True
    elif os.path.exists(os.path.join(currentwrkdir, ".gitignore")):
        printIt = True
    elif os.path.exists(os.path.join(currentwrkdir, "README.md")):
        printIt = True
    elif os.path.exists(os.path.join(currentwrkdir, "src")):
        printIt = True
    if silent:
      printIt = False 
        
    if printIt:
        for file in filesToDel:
            print(f"Warning: This will delete the file: {file}")
        for folder in foldersToDel:
            print(f"Warning: This will delete the folder: {folder}")
        continues = input("This will overwrite existing files in the current directory. Do you want to continue? (y/n): ")
        if continues.lower() != "y":
            sys.exit("Initialization cancelled by user.")
        elif continues.lower() == "y":
            print("Continuing with initialization...")
            
            
    for file in filesToDel:
        try:
            os.remove(os.path.join(currentwrkdir, file))
        except FileNotFoundError:
            pass
    for folder in foldersToDel:
        shutil.rmtree(os.path.join(currentwrkdir, folder), ignore_errors=True)

    # Run Rojo init in the current working directory
    subprocess.run(f"cd {currentwrkdir} && rojo init", shell=True)

    print("Setting up folder structure...")

    # Read the name from the Rojo-generated default.project.json
    old_json_path = os.path.join(currentwrkdir, "default.project.json")
    with open(old_json_path, "r") as f:
        old_json = json.load(f)
    project_name = old_json["name"]

    # Replace the template name with the actual project name
    JsonData["name"] = project_name

    # Remove old src folder and the old default.project.json
    shutil.rmtree(os.path.join(currentwrkdir, "src"), ignore_errors=True)
    os.remove(old_json_path)

    # Write the modified template as the new default.project.json
    with open(old_json_path, "w") as f:
        json.dump(JsonData, f, indent=2)

    # Recreate src folder and subfolders
    srcFolder = os.path.join(currentwrkdir, "src")
    folders = [
        "ReplicatedStorage",
        "ServerScriptService",
        "ServerStorage",
        "StarterPlayer",
        os.path.join("StarterPlayer", "StarterPlayerScripts"),
        os.path.join("StarterPlayer", "StarterCharacterScripts"),
        "StarterGui",
        "StarterPack",
        "SoundService",
        "Lighting",
        "TextChatService",
        "Teams"
    ]

    for folder in folders:
        os.makedirs(os.path.join(srcFolder, folder), exist_ok=True)

    print("Folder structure created!")