from src.agent.engineer.structure.views import Folder, File,Class, Method, Structure
import xml.etree.ElementTree as ET
import re

def extract_xml(text: str) -> str:
    """Extracts XML content inside triple backticks with 'xml'."""
    pattern = r"```xml\n([\s\S]*?)\n```"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else text

def parse_method(method_element):
    """Parses a <Method> XML element into a Method Pydantic object."""
    return Method(
        name=method_element.find("Name").text,
        parameters=[param.text for param in method_element.findall("Parameters/ParameterItem")],
        description=method_element.find("Description").text,
        return_type=method_element.find("ReturnType").text
    )

def parse_class(class_element):
    """Parses a <Class> XML element into a Class Pydantic object."""
    return Class(
        name=class_element.find("Name").text,
        properties=[prop.text for prop in class_element.findall("Properties/PropertyItem")],
        methods=[parse_method(method) for method in class_element.findall("Methods/Method")]
    )

def parse_file(file_element):
    """Parses a <File> XML element into a File Pydantic object."""
    return File(
        name=file_element.find("Name").text,
        description=file_element.find("Description").text,
        path=file_element.find("Path").text,
        imports=[imp.text for imp in file_element.findall("Imports/ImportItem")],
        classes=[parse_class(cls) for cls in file_element.findall("Classes/Class")],
        variables=[var.text for var in file_element.findall("Variables/VariableItem")]
    )

def parse_folder(folder_element):
    """Parses a <Folder> XML element into a Folder Pydantic object."""
    return Folder(
        name=folder_element.find("Name").text,
        files=[parse_file(file) for file in folder_element.findall("Files/File")],
        subfolders=[parse_folder(subfolder) for subfolder in folder_element.findall("Subfolders/Folder")]
    )

def parse_structure(content):
    """Converts XML string into a Pydantic Structure object."""
    xml_content = extract_xml(content)
    root = ET.fromstring(xml_content)
    folder = parse_folder(root.find("Folder"))
    return Structure(folder=folder)


def get_tree(structure:Structure, prefix=""):
    def get_subfolder(subfolder:Folder, prefix):
        tree_str = f"{prefix}📂 {subfolder.name}\n"

        # Add files inside the subfolder
        for file in subfolder.files:
            tree_str += f"{prefix}   📄 {file.name}\n"

        # Recursively add nested subfolders
        for nested_subfolder in subfolder.subfolders:
            tree_str += get_subfolder(nested_subfolder, prefix + "   ")

        return tree_str
    folder = structure.folder  # Extract root folder from the Pydantic model
    tree_str = f"{prefix}📂 {folder.name}\n"

    # Add files in the root folder
    for file in folder.files:
        tree_str += f"{prefix}   📄 {file.name}\n"

    # Recursively add subfolders
    for subfolder in folder.subfolders:
        tree_str += get_subfolder(subfolder, prefix + "   ")

    return tree_str.strip()  # Remove trailing newline for cleaner output