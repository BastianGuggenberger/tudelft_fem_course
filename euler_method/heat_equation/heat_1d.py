import numpy as np
import math
import matplotlib.pyplot as plt

def f(x):
    basis = np.sin(np.pi * x)                                  
    waves = 0.3*np.sin(5*np.pi*x) + 0.15*np.sin(17*np.pi*x)   
    peaks = (0.8*np.exp(-((x-0.2)/0.01)**2)                 
             - 0.6*np.exp(-((x-0.55)/0.008)**2)
             + 0.5*np.exp(-((x-0.8)/0.012)**2))
    return basis + waves + peaks

alpha = 1.0
dx = 0.01
dt = 0.4 * dx**2 / alpha   #important for convergence according to claude


x_vec = np.arange(0,1,dx)
t_vec = np.arange(0,1,dt)

u_vec_x = [f(x) for x in x_vec]
u_vec_x_new = u_vec_x.copy()

plt.ion()
plt.figure()
max = np.array(u_vec_x).max()
plt.ylim(0,max)
for (step,t) in enumerate(t_vec):
    for i in range(1,len(x_vec)-1):
        u_vec_x_new[i] = u_vec_x[i] + dt*alpha * (u_vec_x[i+1] + u_vec_x[i-1] -2*u_vec_x[i])/(dx**2)
    for i, u_new in enumerate(u_vec_x_new):
        u_vec_x[i] = u_new
    if step % 1 == 0:
        if not plt.get_fignums():
            break
        plt.clf()
        plt.plot(x_vec,u_vec_x_new)
        plt.ylim(0,max)
        plt.pause(0.01)

plt.ioff()
plt.show()