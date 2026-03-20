import json
import os
import zipfile
import sys

def build(output_path=None):
    SETTINGS_FILE = "settings.json"
    REQUIRED_FIELDS = ["author", "name", "id"]
    
    if not os.path.exists(SETTINGS_FILE):
        print(f"Error: {SETTINGS_FILE} not found in the current directory. Automatically creating a template {SETTINGS_FILE}...")
        template = {
            "author": "Your Name",
            "name": "Project Name",
            "id": "project-id"
        }

        # create the file and write the template directly
        with open(SETTINGS_FILE, "w") as f:
            json.dump(template, f, indent=2)  # writes the JSON template
        sys.exit("A template settings.json has been created. Please customize it and run the build command again.")
        
        
    with open(SETTINGS_FILE, "r") as f:
        settings = json.load(f)
    
    for field in REQUIRED_FIELDS:
        if field not in settings:
            raise ValueError(f"Missing required field in settings.json: {field}")
    
    project_name = settings["name"]
    
    # Default output path
    if output_path is None:
        cwd = os.getcwd()
        default_json_path = os.path.join(cwd, "default.project.json")
        if os.path.exists(default_json_path):
            with open(default_json_path, "r") as f:
                default_json = json.load(f)
            project_name = default_json.get("name", project_name)
        output_path = os.path.join(cwd, f"{project_name}.crucible")
    
    # Collect files/folders
    files_to_zip = []
    FoldersToZip = ["src"]
    # Add folders (with structure)
    for folder in FoldersToZip:
        if os.path.exists(folder) and os.path.isdir(folder):
            for root, dirs, files in os.walk(folder):
                # Add folder itself
                relative_root = os.path.relpath(root)
                if relative_root != ".":
                    zf_path = relative_root.replace("\\", "/") + "/"
                    files_to_zip.append(zf_path)
                # Add files inside folder
                for file in files:
                    full_path = os.path.join(root, file)
                    relative_path = os.path.relpath(full_path).replace("\\", "/")
                    files_to_zip.append(relative_path)
        else:
            print(f"Warning: {folder} does not exist")
    
    # Create the Crucible package
    with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for path in files_to_zip:
            if path.endswith("/"):  # it's a folder
                zf.writestr(path, "")  # create empty folder entry
            else:
                zf.write(path)
        # Embed settings.json inside the zip
        zf.writestr("settings.json", json.dumps(settings, indent=2))
    
    print(f"Project built successfully! Output: {output_path}")


# Command-line support
if __name__ == "__main__":
    path_arg = sys.argv[1] if len(sys.argv) > 1 else None
    build(path_arg)