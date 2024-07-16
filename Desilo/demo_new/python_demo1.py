import compyler as cp

import numpy as np

# Create a FHE program object
program = cp.FheProgram(scheme="CKKS", devices=[1]) # FheProgram 여기부터 plan.py의 FheProgram Class를 부르는것부터 시작임. 

# Add secret variables. This is a ciphernode.
a = program.add_secret("a", 40) 

# Create a FHE circuit
b = -a + 2

program.cppcompile(b)

"""
b -> b = -a + 2 이 둘은 어떻게 연결되나? 

b가 FreeNode를 inherit하는 CipherNode임.
왜냐면, a에 대한 모든 연산이 재정의 되어있고, interpreter가 작동하면서 
__add__, __negate__등을 호출하고 또 다른 FreeNode를 return했기 때문.
-> 근데 CPP에서는 interpreter가 없으니까... compile해서 돌리기 전까진
overload된 operator의 영향이 발현될 수가 없음. 

1. CPP 소스코드를 위한 interpreter를 만들어서 OP overload의 effect를 만들어내거나,

2. 아니면 Clang AST에서 nxGraph의 DAG로 변환하는 매커니즘을 이해해서 변환기를 작성하거나. 



"""