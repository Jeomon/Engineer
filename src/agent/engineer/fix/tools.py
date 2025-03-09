from src.agent.engineer.fix.views import Shell,Read,Write
from src.tool import Tool
import subprocess
import shlex
import os

@Tool('Write Tool',args_schema=Write)
def write_tool(directory, file_name, content):
    """
    Write the given content to a specified file within a given directory.
    """
    if not os.path.exists(directory):
        os.makedirs(directory)
    file_path = os.path.join(directory, file_name)
    with open(file_path, 'w') as file:
        file.write(content)
    return f"The {file_name} successfully saved to {file_path}"

@Tool('Read Tool',args_schema=Read)
def read_tool(directory,file_name):
    """
    Read the content from a specified file within a given directory.
    """
    file_path = os.path.join(directory, file_name)
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    with open(file_path, 'r') as file:
        content = file.read()
    print(f"Content successfully read from {file_path}")
    return content

@Tool('Shell Tool',args_schema=Shell)
def shell_tool(command, script_args) -> str:
    """
    Execute the shell command, python scripts then return their output.
    """
    try:
        safe_command = shlex.split(command)
        if script_args:
            safe_command.extend(script_args)
        result = subprocess.run(safe_command, capture_output=True, text=True)
        if result.returncode != 0:
            return f"Error: {result.stderr.strip()}"
        return result.stdout.strip()
    except Exception as e:
        return f"Exception occurred: {str(e)}"