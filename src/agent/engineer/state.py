from src.agent.engineer.structure.views import Structure
from typing import TypedDict

class EngineerState(TypedDict):
    title:str
    overview:str
    libraries:list[str]
    tree_structure:str
    input:str
    output:str
    plan_data:str
    structure_data: Structure
    error:str
