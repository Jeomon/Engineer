from pydantic import BaseModel,Field
from src.tool import Tool

class FileReader(BaseModel):
    file_path:str=Field(...,description="The path to the file to be read.",example=['/path/to/file.txt'])

@Tool("File Reader Tool",args_schema=FileReader)
def file_reader_tool(file_path:str):
    '''
    Reads the contents of a file given the file path.
    '''
    try:
        with open(file_path, 'r') as file:
            content = file.read()
            return content
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except Exception as err:
        return f"Error: {err}"
    

class FileWriter(BaseModel):
    file_path:str=Field(...,description="The path where the file will be saved.",example=['/path/to/file.txt'])
    contents:str=Field(...,description="The contents to be saved in the file.",example=['Hello, World!'])

@Tool("File Writer Tool",args_schema=FileWriter)
def file_writer_tool(file_path:str,contents:str)->str:
    '''
    Saves the given contents to the specified file path.
    '''
    try:
        with open(file_path, 'w') as file:
            file.write(contents)
        return f'Contents saved to {file_path}'
    except Exception as err:
        return f'Error: {err}'