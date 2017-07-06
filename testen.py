import numpy as np
import math
import sympy as sp
import matplotlib.pyplot as plt
from scipy.misc import derivative

sampletime=1
Rp=1
Cp=1

I = np.eye(2, dtype='double')

print(I)


List = []
List.append(I)
List.append(Rp)
List.append(I)

print(List[0])
print(List)

tss = np.matrix([[1.0, 2.0], [3.0, 4.0]]); tss

I = np.matrix([[1.0,0.0],[0.0,1.0]])

z = tss.getI()

print(z)





x = sp.Symbol('x')

def f(x):
    return 3.0*x**2 + 1.0


y = sp.diff(3.0*x**2 + 1.0)

print(f(1))


print(derivative(f,2.0))



z= 0.01


p1 =    0.008455  
p2 =     -0.1075  
p3 =    -0.05198  
p4 =      0.3857  
p5 =     0.07347  
p6 =      -0.398  
p7 =    -0.03754  
p8 =     0.06001  
p9 =       3.294


OCV = p1*z**8 + p2*z**7 + p3*z**6 + p4*z**5 + p5*z**4 + p6*z**3 + p7*z**2 + p8*z + p9

print(OCV)

