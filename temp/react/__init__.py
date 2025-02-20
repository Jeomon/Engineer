from src.agent.react.utils import extract_llm_response,read_markdown_file
from src.message import AIMessage,HumanMessage,SystemMessage
from langchain_core.runnables.graph import MermaidDrawMethod
from langgraph.graph import StateGraph,END,START
from src.agent.react.state import AgentState
from IPython.display import display,Image
from src.inference import BaseInference
from src.agent import BaseAgent
from pydantic import BaseModel
from termcolor import colored
from platform import system
from getpass import getuser
from src.tool import Tool
from os import getcwd
from time import sleep
import json

class ReactAgent(BaseAgent):
    def __init__(self,name:str='',description:str='',instructions:list[str]=[],tools:list[Tool]=[],llm:BaseInference=None,max_iteration=10,verbose=False):
        self.name=name
        self.description=description
        self.instructions=self.get_instructions(instructions)
        self.system_prompt=read_markdown_file('./src/agent/react/prompt/react.md')
        self.max_iteration=max_iteration
        self.tool_names=[]
        self.tools_description=[]
        self.tools={}
        self.iteration=0
        self.llm=llm
        self.verbose=verbose
        self.graph=self.create_graph()
        self.add_tools_to_toolbox(tools)

    def get_instructions(self,instructions):
        return '\n'.join([f'{i+1}. {instruction}' for i,instruction in enumerate(instructions)])

    def add_tools_to_toolbox(self,tools:list[Tool]):
        for tool in tools:
            self.tool_names.append(tool.name)
            self.tools_description.append(json.dumps({
                'Tool Name': tool.name,
                'Tool Input': tool.schema if tool.schema.get('properties') else {},
                'Tool Description': tool.description
            },indent=2))
            self.tools[tool.name]=tool

    def reason(self,state:AgentState):
        sleep(60)
        message=self.llm.invoke(state['messages'])
        response=extract_llm_response(message.content)
        thought=response.get('Thought')
        if self.verbose:
            print(colored(f'Thought: {thought}',color='green',attrs=['bold']))
        return {**state,'messages':[message],'agent_data':response}

    def action(self,state:AgentState):
        agent_data=state['agent_data']
        thought=agent_data.get('Thought')
        action_name=agent_data.get('Action Name')
        action_input=agent_data.get('Action Input')
        route=agent_data.get('Route')
        if self.verbose:
            print(colored(f'Action Name: {action_name}',color='cyan',attrs=['bold']))
            print(colored(f'Action Input: {json.dumps(action_input,indent=2)}',color='cyan',attrs=['bold']))
        if action_name not in self.tool_names:
            observation="This tool is not available in the tool box."
        else:
            tool=self.tools[action_name]
            try:
                observation=tool.invoke(**action_input)
            except Exception as e:
                observation=str(e)
        if self.verbose:
            print(colored(f'Observation: {observation}',color='magenta',attrs=['bold']))
        state['messages'].pop()
        messages=[
            AIMessage(f'<Thought>{thought}</Thought>\n<Action Name>{action_name}</Action Name>\n<Action Input>{json.dumps(action_input,indent=2)}</Action Input>\n<Route>{route}</Route>'),
            HumanMessage(f'<Observation>{observation}</Observation>')
        ]
        return {**state,'messages':messages}

    def final(self,state:AgentState):
        if self.max_iteration>self.iteration:
            agent_data=state['agent_data']
            output=agent_data.get('Final Answer')
        else:
            output="The maximum number of iterations has been reached."
        if self.verbose:
            print(colored(f'Final Answer: {output}',color='blue',attrs=['bold']))
        return {**state,'output':output}


    def controller(self,state:AgentState):
        if self.max_iteration>self.iteration:
            self.iteration+=1
            agent_data=state['agent_data']
            return agent_data.get('Route').lower()
        else:
            return 'final'

    def create_graph(self):
        workflow=StateGraph(AgentState)

        workflow.add_node('reason',self.reason)
        workflow.add_node('action',self.action)
        workflow.add_node('final',self.final)

        workflow.add_edge(START,'reason')
        workflow.add_conditional_edges('reason',self.controller)
        workflow.add_edge('action','reason')
        workflow.add_edge('final',END)

        return workflow.compile(debug=False)

    def plot_mermaid(self):
        '''
        Mermaid plot for the agent.
        '''
        plot=self.graph.get_graph().draw_mermaid_png(draw_method=MermaidDrawMethod.API)
        return display(Image(plot))

    def invoke(self,input:str=''):
        if self.verbose:
            print(f'Entering {self.name}')
        parameters={
            'name':self.name,
            'description':self.description,
            'instructions':self.instructions,
            'tools':f'[{',\n'.join(self.tools_description)}]',
            'tool_names':self.tool_names
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f"Question:{input}\n Operating System:{system()}\nUser:{getuser()}\nCWD:{getcwd()}"
        state={
            'input':input,
            'agent_data':{},
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'output':'',
        }
        response=self.graph.invoke(state)
        return response.get('output')

    def stream(self, input: str='',model:BaseModel|None=None):
        if self.verbose:
            print(f'Entering {self.name}')
        parameters={
            'name':self.name,
            'description':self.description,
            'instructions':self.instructions,
            'tools':f'[{',\n'.join(self.tools_description)}]',
            'tool_names':self.tool_names
        }
        system_prompt=self.system_prompt.format(**parameters)
        user_prompt=f"Question:{input}\n Operating System:{system()}\nUser:{getuser()}\nCWD:{getcwd()}"
        state={
            'input':input,
            'agent_data':{},
            'messages':[SystemMessage(system_prompt),HumanMessage(user_prompt)],
            'model':model,
            'output':'',
        }
        events=self.graph.stream(state)
        for event in events:
            for value in event.values():
                if value.get('output'):
                    yield value.get('output')