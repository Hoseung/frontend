import compyler as cp

import numpy as np

# Create a FHE program object
program = cp.FheProgram(scheme="CKKS", devices=[1]) # FheProgram 여기부터 plan.py의 FheProgram Class를 부르는것부터 시작임. 

# Add secret variables. This is a ciphernode.
a = program.add_secret("a", 40) 

# Create a FHE circuit
b = -a + 2

program.cppcompile(b)