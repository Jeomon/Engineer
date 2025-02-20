from src.agent.engineer.develop.views import Develop
import re

def extract_xml(text: str) -> str:
    """Extracts XML content inside triple backticks with 'xml'."""
    pattern = r"```xml\n([\s\S]*?)\n```"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else text

def extract_python(text: str) -> str:
    """Extracts python content inside triple backticks with 'python'."""
    pattern = r"```python\n([\s\S]*?)\n```"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else text

def parse_develop(text: str):
    """Parses XML content and converts it into a Develop object."""
    content={}
    filename_match = re.search(r'<Filename[^>]*>(.*?)</Filename>', text, re.DOTALL)
    if filename_match:
        content['filename'] = filename_match.group(1).strip()
    code_match = re.search(r'<Code[^>]*>(.*?)</Code>', text, re.DOTALL)
    if code_match:
        content['code'] = extract_python(code_match.group(1).strip())
    return Develop(filename=content.get('filename'),code=content.get('code'))