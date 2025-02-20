from pydantic import BaseModel,Field

class Develop(BaseModel):
    filename: str=Field(...,description='The name of the file',examples=['main.py'])
    code: str=Field(...,description='The python script goes here',examples=['print("Hello World")'])