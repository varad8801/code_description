import ast

class CodeDescriptionGenerator(ast.NodeVisitor):
    """
    A class to generate human-readable descriptions of functions in code.
    """
    def __init__(self):
        self.indent = ' ' * 4  # Indentation for descriptions

    def visit_FunctionDef(self, node):
        """
        Visit a function node and generate a detailed description.
        """
        description = self.describe_function(node)
        print(description)
        self.generic_visit(node)

    def describe_function(self, node):
        """
        Generate a detailed description of a function node in plain English.
        """
        description = f"Function '{node.name}' does the following:\n"
        
        # Extract and describe function docstring if present
        docstring = ast.get_docstring(node)
        if docstring:
            description += f"{self.indent}Description: {docstring}\n"
        else:
            description += f"{self.indent}Description: No description provided.\n"

        # Extract function arguments
        args = [arg.arg for arg in node.args.args]
        description += f"{self.indent}Arguments: {', '.join(args)}\n"
        
        # Describe initialization
        initialization = [stmt for stmt in node.body if isinstance(stmt, ast.Assign)]
        if initialization:
            description += f"{self.indent}Initialization:\n"
            for stmt in initialization:
                targets = ", ".join(ast.dump(target) for target in stmt.targets)
                value = ast.dump(stmt.value)
                description += f"{self.indent * 2}Assigns the value {value} to {targets}.\n"

        # Describe error handling
        errors = [stmt for stmt in node.body if isinstance(stmt, ast.Raise)]
        if errors:
            description += f"{self.indent}Error Handling:\n"
            for stmt in errors:
                exception = ast.dump(stmt.exc)
                description += f"{self.indent * 2}Raises an exception: {exception}.\n"
        
        # Describe function body
        processing = [stmt for stmt in node.body if not isinstance(stmt, (ast.Assign, ast.Raise))]
        if processing:
            description += f"{self.indent}Processing:\n"
            for stmt in processing:
                if isinstance(stmt, ast.If):
                    test = ast.dump(stmt.test)
                    description += f"{self.indent * 2}Contains an if statement checking: {test}.\n"
                elif isinstance(stmt, ast.For):
                    target = ast.dump(stmt.target)
                    iter_ = ast.dump(stmt.iter)
                    description += f"{self.indent * 2}Contains a for loop iterating over: {iter_} with target: {target}.\n"
                elif isinstance(stmt, ast.While):
                    test = ast.dump(stmt.test)
                    description += f"{self.indent * 2}Contains a while loop checking: {test}.\n"
                elif isinstance(stmt, ast.Return):
                    value = ast.dump(stmt.value) if stmt.value else "None"
                    description += f"{self.indent * 2}Returns: {value}.\n"
                elif isinstance(stmt, ast.Expr):
                    description += f"{self.indent * 2}Contains an expression: {ast.dump(stmt)}.\n"
        
        return description

def generate_code_description(code):
    """
    Parse the given code and generate human-readable descriptions for each function.
    """
    tree = ast.parse(code)
    description_generator = CodeDescriptionGenerator()
    description_generator.visit(tree)

def main():
    # Update this line with the path to your code file
    #------------------------------------
    file_path = "a.py"  # Change this to your file's name if needed
    #-----------------------------------------------------------------
    # Load the code from the specified file
    with open(file_path, "r") as file:
        code = file.read()
    
    # Generate and print descriptions of the code
    generate_code_description(code)

if __name__ == "__main__":
    main()
