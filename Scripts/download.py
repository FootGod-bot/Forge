import os
import requests
from pathlib import Path


def download(owner, repo, tag="latest", extension=".zip", out_dir="."):
    """
    Download a GitHub release asset.

    owner: repo owner
    repo: repo name
    tag: release tag or "latest"
    extension: file extension to filter (ex: ".zip")
    out_dir: folder to download into
    """

    if tag == "latest":
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    else:
        url = f"https://api.github.com/repos/{owner}/{repo}/releases/tags/{tag}"

    r = requests.get(url)
    r.raise_for_status()
    release = r.json()

    assets = release.get("assets", [])
    if not assets:
        raise Exception("No assets found in this release.")

    chosen = None

    if extension:
        for asset in assets:
            if asset["name"].lower().endswith(extension.lower()):
                chosen = asset
                break
    else:
        chosen = assets[0]

    if not chosen:
        raise Exception(f"No asset found with extension {extension}")

    download_url = chosen["browser_download_url"]
    filename = chosen["name"]

    os.makedirs(out_dir, exist_ok=True)
    filepath = os.path.join(out_dir, filename)

    with requests.get(download_url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    return Path(filepath)


def download_file(url, dest_folder="."):
    os.makedirs(dest_folder, exist_ok=True)

    filename = url.split("/")[-1].split("?")[0]

    filepath = os.path.join(dest_folder, filename)

    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in r.iter_content(chunk_size=8192):
                if chunk:
                    f.write(chunk)
    
    return Path(filepath)

if __name__ == "__main__":
    download(owner="jqlang", repo="jq", tag="jq-1.8.1", extension=".zip", out_dir="./files")
    input("Press Enter to download a specific file...")
    download_file(url="https://github.com/jqlang/jq/releases/download/jq-1.8.1/jq-win64.exe", dest_folder="./files")