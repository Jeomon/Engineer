Generate the comprehensive plan for developing the software application according to the  user's desired specifications. 
Your primary objective is to understand the app's logic, purpose, and it's functionality, then create a detailed plan with documentation for implementing it.

## Instructions
- Be clear, concise, and avoid ambiguity in your explanations.
- Don't include about testing or deployment of the app in the plan.
- Use a modular and scalable design, ensuring the app can be expanded or modified easily.
- For now make the plan for making python based apps.

Respond in the following format:

<PlanContent>
    <Title type='str'>The name of the app to develop (ex: Calculator App)</Title>
    <Overview type='str'>A high-level description of the app (ex: A simple calculator for basic arithmetic operations.)</Overview>
    <Requirements type='str'>The user requirements of the app (ex: I want to be able to add, subtract, multiply, and divide two numbers.)</Requirements>
    <Logic type='str'>The logic about the working of the app (ex: Supports addition, subtraction, multiplication, and division.)</Logic>
    <Libraries type='list[str]'>
    <!-- The python libraries needed for implementing the app (ex: streamlit, numpy, pandas) -->
        <LibraryItem>Library 1</LibraryItem>
        ...
    </Libraries>
    <Plan type='list[str]'>
    <!-- Steps for developing the app (ex: Design the user interface., Develop the backend logic.) -->
        <PlanItem>Step 1 for developing the app</PlanItem>
        ...
    </Plan>
</PlanContent>

Strictly follow the above format and respond nothing else. No additional text, no code block wrapping or explanations are allowed outside of these formats.