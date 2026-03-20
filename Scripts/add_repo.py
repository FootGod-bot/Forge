import os
import shutil
import json
import zipfile
import time
import sys
from pathlib import Path
from Scripts.download import download_file, download  # your helpers

CRUCIBLE_DIR = Path("./.crucible")
TEMP_DIR = CRUCIBLE_DIR / "temp"
LOG_DIR = CRUCIBLE_DIR / "logs"
if getattr(sys, 'frozen', False):
    # Running as a bundled executable
    script_dir = os.path.dirname(sys.executable)
else:
    # Running as a normal Python script
    script_dir = os.path.dirname(os.path.abspath(__file__))
DB_FILE = os.path.join(script_dir, "databases")
DB_DIR = Path(DB_FILE)
def ensure_dirs():
    TEMP_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

def unique_name(dest: Path):
    """Return a unique path by appending (1), (2), etc if exists"""
    if not dest.exists():
        return dest
    stem, ext = dest.stem, dest.suffix
    i = 1
    while True:
        candidate = dest.parent / f"{stem}({i}){ext}"
        if not candidate.exists():
            return candidate
        i += 1

def resolve_db(db_id, package_name):
    for db_file in DB_DIR.glob("*.json"):
        with open(db_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if data.get("Id") == db_id:
                if package_name in data.get("Packages", {}):
                    return data["Packages"][package_name]
                else:
                    raise ValueError(f"Package '{package_name}' not found in DB '{db_id}'")
    raise ValueError(f"Database '{db_id}' not found")

def is_db_reference(source_str):
    # If it's a local Windows path, ignore DB check
    if os.path.isabs(source_str) and (source_str[1:3] == ":/" or source_str[1:3] == ":\\"):
        return False
    # Only treat as DB if it has ":" and is not a URL
    lower = source_str.lower()
    if ":" in source_str and not lower.startswith(("http://", "https://")):
        return True
    return False

def add_package(source_str, silent):
    ensure_dirs()

    # --- Step 0: unwrap list if needed ---
    if isinstance(source_str, list):
        if len(source_str) != 1:
            raise ValueError("Expected single string, got list of length > 1")
        source_str = source_str[0]

    # --- Step 1: DB reference ---
    if is_db_reference(source_str):
        db_id, package_name = source_str.split(":", 1)
        source_str = resolve_db(db_id, package_name)

    # --- Step 2: Prepare temp folder ---
    temp_subdir = TEMP_DIR / f"pkg_{int(time.time()*1000)}"
    temp_subdir.mkdir(parents=True, exist_ok=True)

    # --- Step 3: Download / local file / GitHub repo ---
    if os.path.isfile(source_str):  # Local file
        dest_file = temp_subdir / Path(source_str).name
        shutil.copy2(source_str, dest_file)
    elif source_str.lower().startswith(("http://", "https://")):  # Direct URL
        dest_file = download_file(url=source_str, dest_folder=str(temp_subdir))
    elif "/" in source_str and len(source_str.split("/")) >= 2:  # GitHub repo
        ext = ".crucible"
        repo_part = source_str
        tag = None
        if "@" in source_str:
            repo_part, tag = source_str.split("@", 1)
        owner, repo_name = repo_part.split("/")[:2]
        # download() returns path
        dest_file = download(owner=owner, repo=repo_name, tag=tag or "latest", extension=ext, out_dir=str(temp_subdir))
    else:
        shutil.rmtree(temp_subdir)
        raise ValueError(f"Cannot determine source type for '{source_str}'")

    # --- Step 4: Convert .crucible -> .zip if needed ---
    if dest_file.suffix == ".crucible":
        zip_path = dest_file.with_suffix(".zip")
        dest_file.rename(zip_path)
        dest_file = zip_path

    if not zipfile.is_zipfile(dest_file):
        shutil.rmtree(temp_subdir)
        raise ValueError(f"Downloaded file {dest_file} is not a valid .crucible file")

    # --- Step 5: Extract ---
    extract_dir = temp_subdir / "extracted"
    with zipfile.ZipFile(dest_file, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # --- Step 6: Load settings.json ---
    settings_path = extract_dir / "settings.json"
    if not settings_path.exists():
        shutil.rmtree(temp_subdir)
        raise ValueError("settings.json not found in package")
    with open(settings_path, "r", encoding="utf-8") as f:
        settings = json.load(f)

    log_id = settings.get("id")
    if not log_id:
        shutil.rmtree(temp_subdir)
        raise ValueError("Project 'id' missing in settings.json")

    log_path = LOG_DIR / f"{log_id}.json"
    if log_path.exists():
        shutil.rmtree(temp_subdir)
        raise ValueError(f"Package with id '{log_id}' already added")

    all_copied_files = []
    
    # --- Step 7: Print info and ask if they are sure
    if not silent:
        package = settings.get("name", "")
        author = settings.get("author", "")
        continues = input(f"This will download the package '{package}' by {author}. Do you want to continue? (y/n)  ")

        if continues.lower() == "n":
            shutil.rmtree(TEMP_DIR)
            ensure_dirs()
            sys.exit("Exiting...")
    
    # --- Step 8: Copy / merge folders ---
    include_folders = ["src"]
    for folder in include_folders:
        src_path = extract_dir / folder
        if not src_path.exists():
            continue
        dest_path = Path.cwd() / folder
        for root, dirs, files in os.walk(src_path):
            rel_root = Path(root).relative_to(src_path)
            current_dest = dest_path / rel_root
            current_dest.mkdir(parents=True, exist_ok=True)
            for f in files:
                if f == "settings.json":
                    continue  # skip settings.json
                src_file = Path(root) / f
                dest_file_path = current_dest / f
                if dest_file_path.exists():
                    dest_file_path = unique_name(dest_file_path)
                shutil.copy2(src_file, dest_file_path)
                all_copied_files.append(str(dest_file_path.resolve()))

    # --- Step 9: Write log ---
    log_data = {
        "id": log_id,
        "author": settings.get("author"),
        "name": settings.get("name"),
        "files": all_copied_files
    }
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(log_data, f, indent=4)

    # --- Step 10: Cleanup temp ---
    shutil.rmtree(temp_subdir)

    print(f"Package '{settings.get('name')}' added successfully. Log saved to {log_path}")