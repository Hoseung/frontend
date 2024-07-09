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
    
    # Print the AST
    print_ast(tu.cursor, location=loc, ignore_main=ignore_main)
    return tu

def get_operator_spelling(node):
    # Helper function to get the specific operator spelling
    tokens = list(node.get_tokens())
    if tokens:
        return "".join([token.spelling for token in tokens])    
    return None

def check_for_ciphertext(node, param_name="a"):
    # Check if the node references the parameter "a" and should be marked as CipherNode
    if param_name in node.spelling:
        print("Found ciphertext reference")
        return True
    for child in node.get_children():
        if check_for_ciphertext(child, param_name):
            print("Found ciphertext reference")
            return True
    return False

def parse_mod(fn_cpp, loc=False):
    # Set up the Clang index and translation unit
    index = clang.cindex.Index.create()
    tu = index.parse(fn_cpp, args=['-std=c++14'], options=0) # unsaved_files=[('tmp.cpp', code)])
    
    # Print the AST
    modified_ast = modify_ast(tu.cursor)
    # print_modified_ast(modified_ast, location=loc)
    print_ast(modified_ast, location=loc)
    return tu

def modify_ast(node, param_name="a"):
    """
    <Don't use>
    node is not a Dictionary. It is a Cursor object.
    Adding a Python dictionary to the Cursor object doesn't work.
    """
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


def print_ast(node, depth=0, location=True, param_name="a", ignore_main=True):
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
    
    # Check for ciphertext reference and add CipherNode if necessary
    if check_for_ciphertext(node, param_name):
        cipher_node_info = f"{clang.cindex.CursorKind.UNEXPOSED_EXPR} CipherNode"
        print(f"{indent}  {cipher_node_info}")        
    
    # Print the node information
    print(f"{indent}{node_info}")
    
    # Recursively print the children nodes
    for child in node.get_children():
        if ignore_main and child.kind == clang.cindex.CursorKind.FUNCTION_DECL and child.spelling == "main":
            continue
        # If the child is an unexposed expression, dive deeper
        # if child.kind == clang.cindex.CursorKind.UNEXPOSED_EXPR:
        #     print_ast(child, depth + 1, location=location, param_name=param_name)
        # else:
        #     # Check for "a" in unary and binary operators
        #     if child.kind == clang.cindex.CursorKind.BINARY_OPERATOR:
        #         for argument in child.get_arguments():
        #             print("Argument: ", argument.spelling)
        #         for grandchild in child.get_children():
        #             print_ast(grandchild, depth + 1, location=location, param_name=param_name)
        #     elif child.kind ==clang.cindex.CursorKind.UNARY_OPERATOR:
        #         for grandchild in child.get_children():
        #             if check_for_ciphertext(grandchild, param_name):
        #                 cipher_node_info = f"{clang.cindex.CursorKind.UNEXPOSED_EXPR} CipherNode"
        #                 print(f"{indent}  {cipher_node_info}")
        #             print_ast(grandchild, depth + 1, location=location, param_name=param_name)
        print_ast(child, depth + 1, location=location, param_name=param_name)
