#1d fem solver example

import numpy as np
import matplotlib.pyplot as plt

N = 20 #number of elements
h = 1/N
alpha = 0.0

def f(x):
    return x**2

x_vec = []
for i in range(N+1):
    x_vec.append(i*h)

f_vec = [0 for i in range(N+1)]
for i in range(N):
    #contribution of element i:
    f_vec[i]+= (x_vec[i+1]-x_vec[i])/2 * f(x_vec[i])
    f_vec[i+1]+=(x_vec[i+1]-x_vec[i])/2 * f(x_vec[i+1])
f_vec = np.array(f_vec)

A=np.zeros((N+1,N+1))

for i in range(N):
    #contribution of element i:
    factor = 1/(x_vec[i+1] - x_vec[i])
    A[i,i]      += factor * 1
    A[i+1,i+1]  += factor * 1
    A[i,i+1]    += factor * -1
    A[i+1,i]    += factor * -1

#boundary conditions: dirichlet
A[0,:] = 0
A[0,0] = 1
f_vec[0] = alpha

c = np.linalg.solve(A,f_vec)
print(c)

#----- Plotting -------------

x_fine = np.linspace(0, 1, 200)
u_exact = x_fine/3 - x_fine**4/12   # exact solution of -u'' = x^2, u(0)=0, u'(1)=0

plt.figure(figsize=(8, 5))
plt.plot(x_fine, u_exact, color="black", linewidth=2, label="exact solution")
plt.plot(x_vec, c, "o--", markersize=4, label=f"FEM solution (N = {N})")
plt.title(rf"1D finite element method (linear elements)" "\n"
          rf"$-u''(x) = x^2$,  $u(0) = {alpha:g}$,  $u'(1) = 0$")
plt.xlabel("x")
plt.ylabel("u(x)")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("fem_py_1d.png",dpi=300)