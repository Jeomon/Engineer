from pydantic import BaseModel,Field

class File(BaseModel):
    name: str=Field(...,description='The name of the file',example=['main.py','logic.py','snake.py'])
    description: str=Field(...,description='A brief explanation of the file’s purpose, its role in the app, and how it contributes to the overall functionality.')
    path:str=Field(...,description='The path of the file',example=['./app_name/subfolder1/abc.py'])
    imports: list[str]=Field(description='The libraries or modules in the app to be imported in the file',example=[['Tool','pandas','Food']],default_factory=[])
    classes: list['Class']=Field(description='The classes present in the file',default_factory=[])
    variables: list[str]=Field(description='The variables present in the file',examples=[['constant','settings']],default_factory=[])

    def to_string(self):
        variables=' ,'.join(self.variables)
        classes='\n'.join([cls.to_string() for cls in self.classes])
        imports=' ,'.join(self.imports)
        return f'File: {self.name}\nDescription: {self.description}\nFile Path: {self.path}\nImports: {imports}\nClasses: {classes}\nVariables: {variables}'

class Class(BaseModel):
    name:str=Field(...,description='The name of the class',examples=['Snake'])
    properties:list[str]=Field(description='The properties present in the class',examples=['size','file_size'],default=[])
    methods:list['Method']=Field(description='The methods present in the class',default_factory=[])

    def to_string(self):
        methods='\n'.join([method.to_string() for method in self.methods])
        return f'Class: {self.name}\nProperties: {', '.join(self.properties)}\nMethods:\n{methods}'

class Method(BaseModel):
    name:str=Field(...,description='The name of the method',examples=['move_snake'])
    parameters:list[str]=Field(description='The parameters the of the method',examples=[['snake:Snake','direction:str']],default_factory=[])
    description:str=Field(...,description='The purpose of the method in detail',examples=['This method tells the snake to mov'])
    return_type:str=Field(description='The return type of the method', examples=['int','list[str]','Move'],default_factory=None)

    def to_string(self):
        return f'Method: {self.name}\nParameters: {' ,'.join(self.parameters)}\nDescription: {self.description}\nReturn Type: {self.return_type}'

class Folder(BaseModel):
    name: str = Field(..., description="The name of the folder or the module", examples=["app"])
    files: list[File] = Field(..., description="Files directly inside the current folder")
    subfolders: list["Folder"] = Field(..., description="It contains further subfolders and files")

    class Config:
        # Pydantic needs this for recursive models
        arbitrary_types_allowed = True
        from_attributes = True

class Structure(BaseModel):
    folder:Folder=Field(description='The structure of the app')
