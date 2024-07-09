import clang.cindex
from collections import defaultdict

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
    modified_ast = modify_ast(tu.cursor)
    print_modified_ast(modified_ast, location=loc)
    return tu

def get_operator_spelling(node):
    # Helper function to get the specific operator spelling
    tokens = list(node.get_tokens())
    if tokens:
        return tokens[0].spelling
    return None

def check_for_ciphertext(node, param_name="a"):
    # Check if the node references the parameter "a"
    if node.kind == clang.cindex.CursorKind.DECL_REF_EXPR and node.spelling == param_name:
        return True
    for child in node.get_children():
        if check_for_ciphertext(child, param_name):
            return True
    return False

def modify_ast(node, param_name="a"):
    # Modify the AST to include CipherNode at appropriate places
    modified_children = []
    for child in node.get_children():
        modified_child = modify_ast(child, param_name)
        if child.kind in (clang.cindex.CursorKind.BINARY_OPERATOR, clang.cindex.CursorKind.UNARY_OPERATOR) and check_for_ciphertext(child, param_name):
            # Insert CipherNode
            cipher_node = {
                'kind': 'CipherNode',
                'spelling': '',
                'type': 'Cipher',
                'location': child.location,
                'children': [modified_child]
            }
            modified_children.append(cipher_node)
        modified_children.append(modified_child)

    modified_node = {
        'kind': node.kind,
        'spelling': node.spelling,
        'type': node.type.kind.spelling if node.type.kind != clang.cindex.TypeKind.INVALID else '',
        'location': node.location,
        'children': modified_children
    }
    return modified_node

def print_modified_ast(node, depth=0, location=True):
    # Print the modified AST
    indent = ' ' * (depth * 2)
    
    # Gather additional information about the node
    node_info = f"{node['kind']} {node['spelling']}"
    if node['type']:
        node_info += f" : {node['type']}"
    if location and node['location']:
        node_info += f" [{node['location']}]"
    
    # Print the node information
    print(f"{indent}{node_info}")
    
    # Recursively print the children nodes
    for child in node['children']:
        print_modified_ast(child, depth + 1, location=location)
