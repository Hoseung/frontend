import clang.cindex

def find_functions(node):
    # Recursively find all function declarations in the AST
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        print(f'Found function: {node.spelling}')
    for child in node.get_children():
        find_functions(child)

def parse_code_snippet(fn_cpp, loc=False, ignore_main=True):
    # Set up the Clang index and translation unit
    index = clang.cindex.Index.create()
    tu = index.parse(fn_cpp, args=['-std=c++14'], options=0) # unsaved_files=[('tmp.cpp', code)])
    print_ast(tu.cursor, location=loc, ignore_main=ignore_main)
    return tu

def get_operator_spelling(node):
    # Helper function to get the specific operator spelling
    tokens = list(node.get_tokens())
    if tokens:
        return "".join([token.spelling for token in tokens])    
    return None

def print_ast(node, depth=0, location=True, ignore_main=True):
    # Print the current node with indentation based on depth
    indent = ' ' * (depth * 2)
    
    # Gather additional information about the node
    node_info = f"{node.kind} {node.spelling}"
    if node.type.kind != clang.cindex.TypeKind.INVALID:
        node_info += f" : {node.type.kind.spelling}"    
    # Append specific operator information for binary and unary operators
    if node.kind in (clang.cindex.CursorKind.BINARY_OPERATOR, clang.cindex.CursorKind.UNARY_OPERATOR):
        operator_spelling = get_operator_spelling(node)
        if operator_spelling:
            node_info += f" (Operator: {operator_spelling})"
    if location: 
        node_info += f" [{node.location}]"

    
    # Print the node information
    print(f"{indent}{node_info}")
    
    # Recursively print the children nodes
    for child in node.get_children():
        if ignore_main and child.kind == clang.cindex.CursorKind.FUNCTION_DECL and child.spelling == "main":
            continue
        # If the child is an unexposed expression, dive deeper
        if child.kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
            print_ast(child, depth + 1, location=location)
        else:
            print_ast(child, depth + 1, location=location)
