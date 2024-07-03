import clang.cindex

def find_functions(node):
    # Recursively find all function declarations in the AST
    if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
        print(f'Found function: {node.spelling}')
    for child in node.get_children():
        find_functions(child)

def parse_code_snippet(fn_cpp, loc=False):
    # Set up the Clang index and translation unit
    index = clang.cindex.Index.create()
    tu = index.parse(fn_cpp, args=['-std=c++14'], options=0) # unsaved_files=[('tmp.cpp', code)])
    
    # Print the AST
    print_ast(tu.cursor, location=loc)
    return tu

def print_ast(node, depth=0, location=True):
    # Print the current node with indentation based on depth
    indent = ' ' * (depth * 2)
    
    # Gather additional information about the node
    node_info = f"{node.kind} {node.spelling}"
    if node.type.kind != clang.cindex.TypeKind.INVALID:
        node_info += f" : {node.type.kind.spelling}"
    if location: node_info += f" [{node.location}]"
    
    # Print the node information
    print(f"{indent}{node_info}")
    
    # Recursively print the children nodes
    for child in node.get_children():
        print_ast(child, depth + 1, location=location)