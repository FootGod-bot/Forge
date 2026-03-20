# Crucible Package Manager

A lightweight CLI package manager for roblox.  

## How it works
Crucible is made with python, and built with rojo in mind. Rojo is a syncing software that will copy files from a folder to roblox studio. This package manager allows you to auto-insert scripts where you need them, by running one command

## Features

- Simple CLI (`crucible init`, `crucible add`, `crucible remove`, `crucible build`)  
- Supports remote packages (direct download links / GitHub releases)  
- Tracks installed files for safe removal  
- Local and online database support (JSON-based)  
- Minimal and fast — no bloated dependency system  

---

## Installation

### Install rokit:
visit [rokit](https://github.com/rojo-rbx/rokit/releases) and install the latest version

### Setup repo
Enter the folder You want to run   
run the following commands:  
```bash
rokit init
rokit add rojo
rokit add FootGod-bot/Crucible
Crucible init
```


## Add a repo
To install a Crucible repo, there are three ways to do it. #1 is via the github releases tab, #2 is via a direct link, and you can also use a local file
### Github example
```bash
crucible add user/repo
```
### Direct link example
```bash
crucible add example.com/example.crucible
```
### Local file example
```bash
crucible add "C:/users/admin/downloads/example.crucible"
```

## Remove a repo
To remove a repo, run the following command:
```bash
crucible remove name
```
The name should be printed when you installed the package

## Make your own package
To make your own package, make a new folder, and load it as the only files in the project folder  
Run:
```
crucible build
```
to convert the project to a .Crucible file.

## How to share
To share, the best way is to put it on a github repo. in the main part of the repo, we recomend putting the source code. Then, open the releases tab, and make a new release. It MUST have the tag release to be auto-downloaded by the script.
Then if people run `crucible add YourUser/YourRepo` then it will download the repo (Note, this feature is untested, but you should be able to download a specific version of a repo by adding a @ at the end, then the title of the release)
