import compyler as cp

import numpy as np

# Create a FHE program object
program = cp.FheProgram(scheme="CKKS", devices=[1])

# Add secret variables. This is a ciphernode.
a = program.add_secret("a", 40) 

# Create a FHE circuit
b = a.std()

program.cppcompile(b)