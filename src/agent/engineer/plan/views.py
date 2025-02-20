from pydantic import BaseModel,Field

class Plan(BaseModel):
    title:str=Field(...,description='The name of the app to develop',example=['Calculator'])
    overview:str=Field(...,description='A high-level description of the app',example=['A simple calculator for basic arithmetic operations.'])
    requirements:str=Field(...,description='The user requirements of the app',example=['I want to be able to add, subtract, multiply, and divide two numbers.'])
    logic:str=Field(...,description='The logic about the working of the app',example=['Supports addition, subtraction, multiplication, and division.'])
    libraries:list[str]=Field(description='The python libraries needed for implementing the app',example=[['streamlit','numpy','pandas']],default_factory=[])
    plan:list[str]=Field(...,description='The plan for developing the app',example=['Design the user interface. Develop the backend logic.'])

    def to_string(self):
        plan='\n'.join([f'- {step}' for step in self.plan])
        return f"# Title: {self.title}\n## Overview: {self.overview}\n## Requirements:\n{self.requirements}\n## Logic:\n{self.logic}\n## Plan: {plan}"
