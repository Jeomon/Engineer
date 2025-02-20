from src.agent.engineer.structure.views import Folder
import os

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content

def build_structure(folder: Folder, parent_path: str = ""):
    """
    Recursively creates the folder structure and empty files.
    """
    # Create the current folder
    current_path = os.path.join(parent_path, folder.name)
    os.makedirs(current_path, exist_ok=True)
    
    # Create the files in the current folder
    for file in folder.files:
        file_path = os.path.join(current_path, file.name)
        open(file_path, "w").close()  # Create an empty file
    
    # Recursively create subfolders
    for subfolder in folder.subfolders:
        build_structure(subfolder, current_path)

def iterate_files(folder: Folder):
    """Recursively yield each file from the folder structure."""
    for file in folder.files:
        yield file  # Return one file at a time

    for subfolder in folder.subfolders:
        yield from iterate_files(subfolder)  # Recursively yield files

def write_code(file_path: str, code: str):
    with open(file_path, "w") as f:
        f.write(code)