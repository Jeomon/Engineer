from src.agent.engineer.utils import read_markdown_file, build_structure, iterate_files, write_code
from src.agent.engineer.structure.utils import parse_structure, get_tree
from src.agent.engineer.develop.utils import parse_develop
from src.agent.engineer.plan.utils import parse_plan
from src.message import SystemMessage,HumanMessage
from src.agent.engineer.state import EngineerState
from langgraph.graph import StateGraph,START,END
from src.inference import BaseInference
from subprocess import run,PIPE
from src.agent import BaseAgent
from termcolor import colored

class Engineer(BaseAgent):
    def __init__(self,llm:BaseInference=None,max_iteration=10,verbose=False):
        self.name='Engineer'
        self.description=''
        self.llm=llm
        self.iteration=0
        self.max_iteration=max_iteration
        self.verbose=verbose
        self.graph=self.create_graph()
    
    def plan(self,state:EngineerState):
        plan_prompt=read_markdown_file('src/agent/engineer/plan/prompt.md')
        messages=[SystemMessage(plan_prompt),HumanMessage(state.get('input'))]
        response=self.llm.invoke(messages)
        plan_data=parse_plan(response.content)
        plan='\n'.join([f'{index+1}. {step}' for index,step in enumerate(plan_data.plan)])
        libraries='\n'.join([f'- {library}' for library in plan_data.libraries])
        if self.verbose:
            print(colored(f'Title: {plan_data.title}',color='blue',attrs=['bold']))
            print(colored(f'Overview: {plan_data.overview}',color='green',attrs=['bold']))
            print(colored(f'Requirements: {plan_data.requirements}',color='grey',attrs=['bold']))
            print(colored(f'Logic: {plan_data.logic}',color='yellow',attrs=['bold']))
            print(colored(f'Libraries:\n{libraries}',color='blue',attrs=['bold']))
            print(colored(f'Plan:\n{plan}',color='green',attrs=['bold']))
        return {**state,'title':plan_data.title,'overview':plan_data.overview,'libraries':plan_data.libraries,'plan_data':plan_data.to_string()}

    def structure(self,state:EngineerState):
        structure_prompt=read_markdown_file('src/agent/engineer/structure/prompt.md')
        messages=[SystemMessage(structure_prompt),HumanMessage(state.get('plan_data'))]
        response=self.llm.invoke(messages)
        structure_data=parse_structure(response.content)
        build_structure(structure_data.folder)
        tree_structure=get_tree(structure_data)
        if self.verbose:
            print(colored(f'File structure:\n{tree_structure}',color='cyan',attrs=['bold']))
            print(colored(f'Build the file structure successfully...',color='cyan',attrs=['bold']))
        return {**state,'structure_data':structure_data,'tree_structure':tree_structure}

    def develop(self,state:EngineerState):
        develop_prompt=read_markdown_file('src/agent/engineer/develop/prompt.md')
        root=state.get('structure_data')
        tree_structure=state.get('tree_structure')
        files=[file.to_string() for file in iterate_files(root.folder)]
        user_prompt='## Tree Structure:\n{tree_structure}\n## Files Content:\n{files}\nNow, write the script for the following file.\n{file}'
        for file in iterate_files(root.folder):
            messages=[SystemMessage(develop_prompt),HumanMessage(user_prompt.format(tree_structure=tree_structure,files='\n'.join(files),file=file.to_string()))]
            response=self.llm.invoke(messages)
            print(response.content)
            develop_data=parse_develop(response.content)
            write_code(file.path,develop_data.code)
            if self.verbose:
                print(colored(f'Code written for {file.name} successfully...',color='green',attrs=['bold']))
        return {**state}

    def run(self,state:EngineerState):
        try:
            root_dir=state.get('structure_data').folder
            cmd=['python',f'{root_dir.name}/main.py']
            result = run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                error=f"Error: {result.stderr.strip()}"
            else:
                error=''
        except Exception as e:
            error=f"Error: {e}"
        if self.verbose:
            print(colored(f'Error occurred: {error}',color='red',attrs=['bold']))
        return {**state,'error':error}

    def fix(self):
        pass

    def test(self):
        pass

    def create_graph(self):
        graph=StateGraph(EngineerState)
        graph.add_node('plan',self.plan)
        graph.add_node('structure',self.structure)
        graph.add_node('develop',self.develop)
        graph.add_node('run',self.run)

        graph.add_edge(START,'plan')
        graph.add_edge('plan','structure')
        graph.add_edge('structure','develop')
        graph.add_edge('develop','run')
        graph.add_edge('run',END)

        return graph.compile(debug=False)

    def invoke(self, input):
        state={
            'input':input,
            'title':'',
            'overview':'',
            'output':'',
            'structure_data':None,
            'plan_data':'',
            'error':''
        }
        graph_response=self.graph.invoke(state)
        return graph_response

    def stream(self, input):
        pass



    