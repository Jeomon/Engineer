from pydantic import BaseModel,Field
from typing import Optional,List

class Shell(BaseModel):
    command: str = Field(..., description="The shell command to be executed.")
    script_args: Optional[List[str]] = Field(description="Optional arguments for the shell command.")

class Read(BaseModel):
    directory: str = Field(..., description="The directory where the file is located.")
    file_name: str = Field(..., description="The name of the file to read the content from.")

class Write(BaseModel):
    directory: str = Field(..., description="The directory where the file should be saved.")
    file_name: str = Field(..., description="The name of the file to write the content in.")
    content: str = Field(..., description="The content to be written to the file.")