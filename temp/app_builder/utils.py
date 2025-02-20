import re
import ast
import os

def read_markdown_file(file_path: str) -> str:
    with open(file_path, 'r',encoding='utf-8') as f:
        markdown_content = f.read()
    return markdown_content

def extract_plan(text):
    # Initialize dictionary to store the extracted plan
    plan = {}

    # Extract <Title>
    title_match = re.search(r"<Title>(.*?)</Title>", text, re.DOTALL)
    if title_match:
        plan['title'] = title_match.group(1).strip()

    # Extract <Overview>
    overview_match = re.search(r"<Overview>(.*?)</Overview>", text, re.DOTALL)
    if overview_match:
        plan['overview'] = overview_match.group(1).strip()

    # Extract <Goals>
    goals_match = re.search(r"<Goals>(.*?)</Goals>", text, re.DOTALL)
    if goals_match:
        # Split the goals into a list by newlines or commas
        goals = [goal.strip() for goal in re.split(r'[\n,]', goals_match.group(1)) if goal.strip()]
        plan['goals'] = goals

    # Extract <Structure>
    structure_match = re.search(r"<Structure>(.*?)</Structure>", text, re.DOTALL)
    if structure_match:
        plan['app_structure'] = structure_match.group(1).strip()

    # Extract <Files>
    files = []
    file_matches = re.findall(r"<File>(.*?)</File>", text, re.DOTALL)
    for file_text in file_matches:
        file_data = {}

        # Extract <FileName>
        file_name_match = re.search(r"<Name>(.*?)</Name>", file_text, re.DOTALL)
        if file_name_match:
            file_data['name'] = file_name_match.group(1).strip()

        # Extract <FilePath>
        file_path_match = re.search(r"<Path>(.*?)</Path>", file_text, re.DOTALL)
        if file_path_match:
            file_data['path'] = file_path_match.group(1).strip()

        # Extract <FileDescription>
        file_description_match = re.search(r"<Description>(.*?)</Description>", file_text, re.DOTALL)
        if file_description_match:
            file_data['description'] = file_description_match.group(1).strip()

        files.append(file_data)

    if files:
        plan['files'] = files

    return plan

def extract_file(text):
    pattern = re.compile(
        r"<File>\s*"
        r"<Name>(.*?)<\/Name>\s*"
        r"<Code>(.*?)<\/Code>\s*"
        r"<\/File>",
        re.DOTALL
    )
    match = pattern.search(text)

    if match:
        return {
            'name': match.group(1).strip(),
            'code': match.group(2).strip()
        }
    else:
        return None
    
def tree_structure_to_dict(tree):
    lines = tree.strip().split("\n")
    structure = {}
    stack = [(structure, -1)]  # Stack to hold current dictionary and its indentation level

    for line in lines:
        stripped_line = line.strip()
        current_indent = len(line) - len(stripped_line)

        # Pop from stack until we find the correct parent level
        while stack and stack[-1][1] >= current_indent:
            stack.pop()

        # Add the current item to the parent's dictionary
        current_dict = stack[-1][0]
        if '.' not in stripped_line:  # It's a folder
            current_dict[stripped_line] = {}
            stack.append((current_dict[stripped_line], current_indent))
        else:  # It's a file
            current_dict[stripped_line] = None

    return structure


def create_app_structure(structure, root=''):
    for name, content in structure.items():
        path = os.path.join(root, name)

        if isinstance(content, dict):
            # If the value is a dictionary, it's a folder
            os.makedirs(path, exist_ok=True)
            # Recursively create the contents of the folder
            create_app_structure(content, path)
        else:
            # If the value is None, create an empty file
            if content is None:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write("")  # Create an empty file
                    