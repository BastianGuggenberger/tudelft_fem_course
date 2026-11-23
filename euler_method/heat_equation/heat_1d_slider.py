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
u_vec_history_expl = []
u_vec_history_impl = []
u_vec_x_new = u_vec_x.copy()


# explicit euler
max = np.array(u_vec_x).max()
for step in range(len(t_vec)):
    for i in range(1,len(x_vec)-1):
        u_vec_x_new[i] = u_vec_x[i] + dt*alpha * (u_vec_x[i+1] + u_vec_x[i-1] -2*u_vec_x[i])/(dx**2)
    for i, u_new in enumerate(u_vec_x_new):
        u_vec_x[i] = u_new
    u_vec_history_expl.append(u_vec_x.copy())




#---------plotting


from matplotlib.widgets import Slider

hist = np.array(u_vec_history_expl)
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.2, top=0.82)
line, = ax.plot(x_vec, hist[0])
ax.set_ylim(hist.min() - 0.1, hist.max() + 0.1)
ax.set_xlabel("x")
ax.set_ylabel("T")

fig.suptitle(
    "Explicit Euler for the heat equation\n"
    rf"$\partial_t T(x,t) = \alpha\,\partial_x^2 T(x,t)$,  $\alpha = {alpha}$",
    y=0.98
)

n = len(hist)
slider_ax = fig.add_axes([0.15, 0.05, 0.7, 0.04])
slider = Slider(slider_ax, "log10(step+1)", 0, np.log10(n), valinit=0)

def update(val):
    k = min(int(round(10**slider.val)) - 1, n - 1)
    line.set_ydata(hist[k])
    ax.set_title(f"t = {(k+1)*dt:.5f}  (step {k})")
    fig.canvas.draw_idle()

slider.on_changed(update)
update(0)
plt.show()