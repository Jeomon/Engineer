from src.inference.gemini import ChatGemini
from src.agent.engineer import Engineer
from dotenv import load_dotenv
import os

load_dotenv()
api_key=os.environ.get('GOOGLE_API_KEY')
llm=ChatGemini(model='gemini-2.0-flash',api_key=api_key,temperature=0)
query=input('Enter about the app: ')
engineer=Engineer(llm=llm,verbose=True)
response=engineer.invoke(query)
print(response)