def cpp_fun_to_python(cpp_code, scale=40):
    """
    CPP to Python converter for ordinary CPP syntax
    
    Ciphertext fun(Ciphertext a) {
    // Create FHE circuit
    auto b = -a + 2;
    auto c = a;

    for (int i = 0; i < 5; ++i) {
        c = c * (-c + 2);
        b = b * (-c + 2);
    }

    auto d = b.mean() + c.mean();
    return d;
    }
    """
    cpp_lines = cpp_code.strip().splitlines()
    python_code = ""

    for line in cpp_lines:
        line = line.strip()
        if line.startswith("Ciphertext fun("):
            # Translate function declaration to adding secret
            func_signature = line.split("(")[1].split(")")[0].strip()
            var_name = func_signature.split()[1]
            python_code += f'a = program.add_secret("{var_name}", {scale})\n'
        elif line.startswith("auto "):
            # Translate auto assignment to Python
            var_name, expression = line[5:].split(" = ")
            python_code += f"{var_name.strip()} = {expression.strip()}\n"
        elif line.startswith("for ("):
            # Translate C++ for loop to Python
            loop_header = line[4:].strip("() ")
            init, condition, increment = loop_header.split(";")
            var_name = init.split()[1]
            start_value = init.split("=")[1].strip()
            end_value = condition.split("<")[1].strip()
            # Set increment step
            increment_step = "1" if "++" in increment else increment.split()[-1]
            python_code += f"for {var_name} in range({start_value}, {end_value}, {increment_step}):\n"
        elif line.startswith("return "):
            # Translate return statement to program.cppcompile
            return_var = line.split()[1]  # Get the variable name
            python_code += f"program.cppcompile({return_var})\n"
        elif line.startswith("}"):
            # Ignore closing curly brackets
            continue
        elif line:  # Handle lines with actual code
            python_code += f"    {line}\n"  # Add proper indentation

    # Remove all semicolons from the final Python code
    python_code = python_code.replace(";", "")
    python_code = python_code.replace("//", "#")
    
    return python_code



def compile_cpp_fun(cpp_code, scale=40):
    # Convert the C++ code to Python
    python_code = cpp_fun_to_python(cpp_code, scale)
    
    # Add the Program initialization
    full_python_code = """
import compyler as cp
program = cp.FheProgram(scheme="CKKS", devices=[1])
""" + python_code
    
    # Print the full Python code to check
    print("Full Python code:")
    print(full_python_code)
    
    # # Create a dictionary to capture the local variables
    # local_vars = {}
    
    # Execute the full Python code with the local_vars dictionary
    exec(full_python_code)


def load_cpp_fun(path, fun_name="fun"):
    """
    Load CPP function from file as string.
    Extract only the function with the given name.
    """
    with open(path, "r") as f:
        cpp_code = f.read()    
        
    return extract_fun_function(cpp_code, function_name=fun_name)
        
        
        
import re

def extract_fun_function(cpp_code, function_name="fun"):
    """
    Extracts the function named 'fun' from the C++ code.
    """
    # Define the regular expression pattern to match the function 'fun'
    pattern = re.compile(rf"Ciphertext\s+{function_name}\s*\(.*?\)\s*\{{.*?return\s+.*?;", re.DOTALL)
    match = pattern.search(cpp_code)
    if match:
        fun_code = match.group()
        return fun_code
    else:
        return None
    
    
    
## auto, ;, // 삭제. 
# {}는 분석 후에 삭제. 
# Ciphertext a -> add_secret("a", 40)로 대체.
# scale = 40이라는 정보를 C++ 스럽게 집어넣을 방법이 없음. 
# return b; -> program.cppcompile(b)로 대체.

# 비정상적인 CPP 코드일 경우 에러 나와야 하므로, 제대로 된 CPP 파서로 체크 필요. 