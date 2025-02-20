from typing import TypedDict,Annotated
from src.message import BaseMessage
from operator import add
from pydantic import BaseModel

class AgentState(TypedDict):
    input:str
    agent_data:dict
    messages:Annotated[list[BaseMessage],add]
    output:str