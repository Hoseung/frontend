import compyler as cp

import numpy as np

# Create a FHE program object
program = cp.FheProgram(scheme="CKKS", devices=[1])

# Add secret variables. This is a ciphernode.
a = program.add_secret("a", 40) 

# Create a FHE circuit
b = -a + 2
c = a + 0
for i in range(5):
    c = c * (-c + 2)
    b = b * (-c + 2)
d = b.mean() + c.mean()

program.cppcompile(d)