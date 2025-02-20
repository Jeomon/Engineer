from src.agent.engineer.plan.views import Plan
import xml.etree.ElementTree as ET
import re

def extract_xml(text: str) -> str:
    """Extracts XML content inside triple backticks with 'xml'."""
    pattern = r"```xml\n([\s\S]*?)\n```"
    match = re.search(pattern, text)
    return match.group(1).strip() if match else text

def parse_xml_element(element):
    """Helper function to extract text or list items from an XML element."""
    if not list(element):  # If no children, return text
        return element.text.strip() if element.text else ""
    
    # If element has children, return a list of their text content
    return [child.text.strip() for child in element]

def parse_plan(content: str) -> Plan:
    """Parses XML content and converts it into a Plan object."""
    xml_content = extract_xml(content)
    root = ET.fromstring(xml_content)
    
    title = root.findtext("Title", "").strip()
    overview = root.findtext("Overview", "").strip()
    requirements = root.findtext("Requirements", "").strip()
    logic = root.findtext("Logic", "").strip()
    
    libraries_element = root.find("Libraries")
    libraries = parse_xml_element(libraries_element) if libraries_element is not None else []
    
    plan_element = root.find("Plan")
    plan = parse_xml_element(plan_element) if plan_element is not None else []

    return Plan(
        title=title,
        overview=overview,
        requirements=requirements,
        logic=logic,
        libraries=libraries,
        plan=plan
    )
