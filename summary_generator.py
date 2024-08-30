import ast

class CodeDescriptionGenerator(ast.NodeVisitor):
    """
    A class to generate human-readable descriptions of code functions.
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
        Generate a description of a function node in plain English.
        """
        description = f"Function '{node.name}' does the following:\n"

        # Extract function arguments
        args = [arg.arg for arg in node.args.args]
        description += f"{self.indent}1. It takes the following arguments: {', '.join(args)}.\n"

        # Extract and describe function body
        for stmt in node.body:
            if isinstance(stmt, ast.Assign):
                targets = ", ".join(self.get_expr_string(target) for target in stmt.targets)
                value = self.get_expr_string(stmt.value)
                description += f"{self.indent}2. Assigns the value {value} to {targets}.\n"
            elif isinstance(stmt, ast.If):
                condition = self.get_expr_string(stmt.test)
                description += f"{self.indent}3. Contains an if statement that checks if {condition}.\n"
                description += f"{self.indent}{self.indent}The following statements execute if the condition is true:\n"
                for body_stmt in stmt.body:
                    description += f"{self.indent}{self.indent}{self.describe_statement(body_stmt)}\n"
                if stmt.orelse:
                    description += f"{self.indent}{self.indent}Otherwise, the following statements execute:\n"
                    for orelse_stmt in stmt.orelse:
                        description += f"{self.indent}{self.indent}{self.describe_statement(orelse_stmt)}\n"
            elif isinstance(stmt, ast.For):
                target = self.get_expr_string(stmt.target)
                iter_ = self.get_expr_string(stmt.iter)
                description += f"{self.indent}4. Contains a for loop iterating over {iter_} with target {target}.\n"
                description += f"{self.indent}{self.indent}The following statements execute within the loop:\n"
                for body_stmt in stmt.body:
                    description += f"{self.indent}{self.indent}{self.describe_statement(body_stmt)}\n"
            elif isinstance(stmt, ast.While):
                condition = self.get_expr_string(stmt.test)
                description += f"{self.indent}5. Contains a while loop that continues while {condition}.\n"
                description += f"{self.indent}{self.indent}The following statements execute within the loop:\n"
                for body_stmt in stmt.body:
                    description += f"{self.indent}{self.indent}{self.describe_statement(body_stmt)}\n"
            elif isinstance(stmt, ast.Return):
                value = self.get_expr_string(stmt.value) if stmt.value else "None"
                description += f"{self.indent}6. Returns {value}.\n"
            elif isinstance(stmt, ast.Expr):
                description += f"{self.indent}7. Contains an expression: {self.get_expr_string(stmt)}.\n"

        return description

    def describe_statement(self, stmt):
        """
        Generate a plain-English description of a statement.
        """
        if isinstance(stmt, ast.Assign):
            targets = ", ".join(self.get_expr_string(target) for target in stmt.targets)
            value = self.get_expr_string(stmt.value)
            return f"Assigns the value {value} to {targets}."
        elif isinstance(stmt, ast.If):
            condition = self.get_expr_string(stmt.test)
            return f"Contains an if statement that checks if {condition}."
        elif isinstance(stmt, ast.For):
            target = self.get_expr_string(stmt.target)
            iter_ = self.get_expr_string(stmt.iter)
            return f"Contains a for loop iterating over {iter_} with target {target}."
        elif isinstance(stmt, ast.While):
            condition = self.get_expr_string(stmt.test)
            return f"Contains a while loop that continues while {condition}."
        elif isinstance(stmt, ast.Return):
            value = self.get_expr_string(stmt.value) if stmt.value else "None"
            return f"Returns {value}."
        elif isinstance(stmt, ast.Expr):
            return f"Contains an expression: {self.get_expr_string(stmt)}."
        return "Contains an unknown statement."

    def get_expr_string(self, expr):
        """
        Convert an AST expression to a string.
        """
        if isinstance(expr, ast.Name):
            return f"'{expr.id}'"
        elif isinstance(expr, ast.Constant):
            return f"'{expr.value}'"
        elif isinstance(expr, ast.BinOp):
            left = self.get_expr_string(expr.left)
            right = self.get_expr_string(expr.right)
            op = self.get_op_string(expr.op)
            return f"{left} {op} {right}"
        elif isinstance(expr, ast.Call):
            func = self.get_expr_string(expr.func)
            args = ", ".join(self.get_expr_string(arg) for arg in expr.args)
            return f"Call to {func} with arguments ({args})"
        # Add more expression types if needed
        return str(expr)

    def get_op_string(self, op):
        """
        Convert an AST operator to a string.
        """
        if isinstance(op, ast.Add):
            return "+"
        elif isinstance(op, ast.Sub):
            return "-"
        elif isinstance(op, ast.Mult):
            return "*"
        elif isinstance(op, ast.Div):
            return "/"
        # Add more operators if needed
        return str(op)

def generate_code_description(code):
    """
    Parse the given code and generate human-readable descriptions.
    """
    tree = ast.parse(code)
    description_generator = CodeDescriptionGenerator()
    description_generator.visit(tree)

def main():
    # Update this line with the path to your code file
    file_path = "a.py"  # Change this to your file's name if needed
    
    # Load the code from the specified file
    with open(file_path, "r") as file:
        code = file.read()
    
    # Generate and print descriptions of the code
    generate_code_description(code)

if __name__ == "__main__":
    main()
