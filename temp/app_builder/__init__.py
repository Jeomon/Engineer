from src.agent.app_builder.utils import read_markdown_file,extract_plan,extract_file,create_app_structure,tree_structure_to_dict
from src.agent.app_builder.tools import file_reader_tool,file_writer_tool
from src.message import SystemMessage,HumanMessage
from src.agent.app_builder.state import AgentState
from langgraph.graph import StateGraph,START,END
from src.inference import BaseInference
from src.agent.react import ReactAgent
from src.agent import BaseAgent
from subprocess import run,PIPE
from termcolor import colored
from time import sleep

class Engineer(BaseAgent):
    def __init__(self,llm:BaseInference=None,verbose=False):
        self.name='App Builder'
        self.description=''
        self.llm=llm
        self.verbose=verbose
        self.graph=self.create_graph()

    def plan(self,state:AgentState):
        system_prompt=read_markdown_file('src/agent/app_builder/prompt/planner.md')
        user_prompt=f'Task: {state.get('input')}'
        response=self.llm.invoke([SystemMessage(system_prompt),HumanMessage(user_prompt)])
        plan_data=extract_plan(response.content)
        if self.verbose:
            print(colored(f'App Name: {plan_data.get('title')}',color='blue'))
            print(colored(f'Overview: {plan_data.get('overview')}',color='green'))
            print(colored('Goals',color='yellow'))
            for goal in plan_data.get('goals'):
                print(colored(goal,color='yellow'))
        return {**state,'app_name':plan_data.get('title'),'app_structure':plan_data.get('app_structure'),'files':plan_data.get('files')}
    
    def structure(self,state:AgentState):
        app_structure=state.get('app_structure')
        if self.verbose:
            print(colored(f'App Structure:\n{app_structure}',color='magenta'))
        dict_structure=tree_structure_to_dict(app_structure)
        create_app_structure(dict_structure)
        print(colored('App Structure is created successfully.',color='blue'))
        return state
    
    def code(self,state:AgentState):
        files=[{'name':file.get('name'),'description':file.get('description')} for file in state.get('files')]
        tree_structure=state.get('app_structure')
        system_prompt=read_markdown_file('src/agent/app_builder/prompt/coder.md')
        user_prompt='Tree Structure:\n{tree_structure}Files:\n{files}\nNow, write the content for the following file.\nFile: {name}\nDescription: {description}\n'
        for file in state.get('files'):
            name=file.get('name')
            path=file.get('path')
            description=file.get('description')
            parameters={'name':name,'description':description,'tree_structure':tree_structure,'files':files}
            response=self.llm.invoke([SystemMessage(system_prompt),HumanMessage(user_prompt.format(**parameters))])
            file_data=extract_file(response.content)
            with open(path,'w') as fs:
                code=file_data.get('code')
                fs.write(code)
            print(colored(f'Code written for {name}.',color='green'))
            sleep(60)
        return state
    
    def execute(self,state:AgentState):
        print(colored("Running the app...", color='yellow'))
        app_name=state.get('app_structure').split('\n')[0]
        process = run(['python',f'./{app_name}/main.py'],text=True,stderr=PIPE)    
        if process.returncode != 0:
            error=process.stderr
            print(colored(f"Error occurred: {error}", color='red'))
        else:
            error=''
            print(colored(f"Process executed successfully", color='green'))
        return {**state,'error':error}

    def debug(self,state:AgentState):
        error=state.get('error')
        tree_structure=state.get('app_structure')
        files=[{'name':file.get('name'),'description':file.get('description')} for file in state.get('files')]
        user_prompt="Tree Structure:\n{tree_structure}Files:\n{files}\nFollowing is the error encountered when ran the app.\n{error}\nNow can you fix the error."
        description='You are tasked to fix the error that encountered while running the application. So finding the file that causing the problem and fix it.'
        instructions=[
            'You are given with the tree structure and files with contents of the app, to familiarize yourself with the app',
            'Analysis the error that is given to you and use the file reader tool to read the correct file that causing the problem',
            'Rewrite the code for that file correctly such that no further error occurs because of fixing'
        ]
        agent=ReactAgent('Debug Agent',description=description,instructions=instructions,tools=[file_reader_tool,file_writer_tool],llm=self.llm,verbose=self.verbose)
        parameters={'tree_structure':tree_structure,'files':files,'error':error}
        agent.invoke(user_prompt.format(**parameters))
        return {**state,'error':''}

    def controller(self,state:AgentState):
        if state.get('error'):
            return 'debug'
        else:
            return 'final'
    
    def final(self,state:AgentState):
        pass
    
    def create_graph(self):
        graph=StateGraph(AgentState)
        graph.add_node('plan',self.plan)
        graph.add_node('structure',self.structure)
        graph.add_node('code',self.code)
        graph.add_node('execute',self.execute)
        graph.add_node('debug',self.debug)
        graph.add_node('final',self.final)

        graph.add_edge(START,'plan')
        graph.add_edge('plan','structure')
        graph.add_edge('structure','code')
        graph.add_edge('code','execute')
        graph.add_conditional_edges('execute',self.controller)
        graph.add_edge('debug','execute')
        graph.add_edge('final',END)

        return graph.compile()

    def invoke(self, input):
        state={
            'input':input,
            'app_structure':'',
            'app_state':'',
            'error':'',
            'files':[],
            'output':''
        }
        return self.graph.invoke(state)

    def stream(self, input):
        pass
