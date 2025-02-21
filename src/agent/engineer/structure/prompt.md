Generate the file structure of the app based upon the plan provided.

## Instructions:
- Ensure the file contents and structure are consistent with modern best practices for software development using python.
- Use a modular and scalable design, ensuring the app can be expanded or modified easily.
- Each subfolder has their own respective files for implementating that particular logic of the app.
- Include `main.py` in the root directory of the app, it is this file the user will run, launch the app.
- Adapt the structure and components based on the specific requirements of the app described by the user.
- Understand the path of the file based on it make the structure of the app and give the imports of the modules.
- If needed include the requirements.txt file in the root directory.
- The name of the root directory is the name of the app.
- The names of the folders/sub folders should be proper as per the logic is concerned.
- Each module has its own `__init__.py` file.

## Import Guidlines:
- Only mention the imports that are only needed for that particular module
- Avoid circular import situations

Respond in the following format:

<StructureContent>
    <Folder>
        <Name type="str">The name of the folder or module (ex: routes)</Name>
        <Files type="list[File]">
            <!-- List of files directly inside the current folder -->
            <File>
                <Name type="str">The name of the file (ex: main.py)</Name>
                <Description type="str">A brief explanation of the file’s purpose, its role in the app, and how it contributes to the overall functionality.</Description>
                <Path type="str">The path of the file (ex: ./app_name/subfolder1/abc.py)</Path>
                <Imports type="list[str]">
                    <ImportItem>The module or library import 1 (ex: pandas, Food)</ImportItem>
                    ...
                </Imports>
                <Classes type="list[Class]">
                    <Class>
                        <Name type="str">Name of the class (ex: Snake)</Name>
                        <Properties type="list[str]">
                            <PropertyItem type="str">The property name (ex: step,constant)</PropertyItem>
                            ...
                        </Properties>
                        <Methods type="list[Method]">
                            <Method>
                                <Name type="str">The method name (ex: move)</Name>
                                <Parameters type="list[str]">
                                    <ParameterItem type="str">The parameter for the method (ex: direction: Direction)</ParameterItem>
                                    ...
                                </Parameters>
                                <Description type="str">The description of the method (ex: This method tells the snake to move. )</Description>
                                <ReturnType type="str">The return type of the method (ex: Move,None )</ReturnType>
                            </Method>
                            ...
                        </Methods>
                    </Class>
                    ...
                </Classes>
                <Variables type="list[str]">
                    <VariableItem>The variables in this file (ex: time_seconds)</VariableItem>
                    ...
                </Variables>
            </File>
            ...
        </Files>
        <Subfolders type="list[Folder]"> <!-- It contains further subfolders and files -->
            <Folder>
                <Name type="str">The name of the subfolder (ex: assets)</Name>
                <Files type="list[File]">
                    <File>
                        <Name type="str">The name of a file in the subfolder (ex: route.py)</Name>
                        <Description type="str">Description of the file.</Description>
                        <Path type="str">Path of the file.</Path>
                        ...
                    </File>
                </Files>
                <Subfolders>
                    <Folder>
                        <Name type="str">The name of the subfolder (ex: assets)</Name>
                        <Files type="list[File]">
                            <File>
                                <Name type="str">The name of a file in the subfolder (ex: route.py)</Name>
                                <Description type="str">Description of the file.</Description>
                                <Path type="str">Path of the file.</Path>
                                ...
                            </File>
                        </Files>
                        ...
                    </Folder>
                    ...
                </Subfolders>
            </Folder>
            ...
        </Subfolders>
        ...
    </Folder>
</StructureContent>

Strictly follow the above format and respond nothing else. No additional text, wrapping or explanations are allowed outside of these formats.