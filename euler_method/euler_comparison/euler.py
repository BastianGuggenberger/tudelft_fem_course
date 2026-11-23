#Implicit and Explicit Euler for a simple differential equation
#DE: f'(x) = a*f(x)

import math
import numpy as np
import matplotlib.pyplot as plt

a=1.0
dt = 0.1


#exact:
def f(x):
    return math.exp(a*x)

ts = np.arange(0,1,dt)
u_ect = [f(t) for t in ts]

#implicit euler:
u_k = 1
u_implct = []
for t in ts:
    u_implct.append(u_k)
    u_k = u_k/(1-a*dt)
u_implct = np.array(u_implct)

#explicit euler:
u_k = 1
u_explct = []
for t in ts:
    u_explct.append(u_k)
    u_k = u_k + dt*a*u_k
u_explct = np.array(u_explct)


#------Plot: -------------------------------------
plt.figure(figsize=(8, 5))
plt.plot(ts, u_ect, color="black", linewidth=2, label="exact: $e^{at}$")
plt.plot(ts, u_implct, "o--", markersize=4, label="implicit Euler")
plt.plot(ts, u_explct, "s--", markersize=4, label="explicit Euler")

plt.title("Implicit vs. explicit Euler method\n$f'(x) = a \\cdot f(x)$, $a = 1$, $\\Delta t = 0.1$")
plt.xlabel("t")
plt.ylabel("u")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig("plot.png", dpi=300)
plt.close()