from typing import TypedDict

class AgentState(TypedDict):
    input:str
    app_structure:str
    app_name:str
    error:str
    files:list[dict]
    output:str