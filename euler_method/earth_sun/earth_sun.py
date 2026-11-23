# demonstration of the explicit euler method
# simulation of the earth falling into the sun due to a sudden stop of its movement

import numpy as np
import matplotlib.pyplot as plt

dt = 60*60
r_vec = []
t_vec = []

r = 149597870000
v = 0
t = 0


mG = 1.9884 * 6.67e19

it = 0
while(r>0):
    it += 1
    #print(r)
    r_vec.append(r/(10**9))
    t_vec.append(t)
    v += - mG * 1/(r*r) * dt
    r += v*dt
    t += dt / (24*60*60) #time in days

print(f"Estimate (Euler): {t:.1f} days")





# Analytical free-fall time (radial Kepler orbit) for comparison
t_analytic = np.pi / 2 * np.sqrt((149_597_870_000) ** 3 / (2 * mG)) / (24 * 60 * 60)
print(f"Analytical:       {t_analytic:.1f} days")


# --- Plot --------------------------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5), dpi=150)

ax.plot(t_vec, r_vec, color="#1f77b4", linewidth=2.2, label="Explicit Euler method (dt = 1 h)")
ax.axvline(t_analytic, color="gray", linestyle="--", linewidth=1.2,
           label=f"Analytical fall time ≈ {t_analytic:.1f} days")

# Mark start and end point
ax.scatter([t_vec[0]], [r_vec[0]], color="#2ca02c", zorder=5, s=50)
ax.annotate("Start: 1 AU\n(v = 0)", (t_vec[0], r_vec[0]),
            xytext=(12, -38), textcoords="offset points", color="#2ca02c")
ax.scatter([t_vec[-1]], [r_vec[-1]], color="#d62728", zorder=5, s=50)
ax.annotate(f"Impact after\n≈ {t:.1f} days", (t_vec[-1], r_vec[-1]),
            xytext=(-95, 40), textcoords="offset points", color="#d62728",
            arrowprops=dict(arrowstyle="->", color="#d62728"))

ax.set_title("Earth falling into the Sun\nDemonstration of the explicit Euler method", fontsize=13)
ax.set_xlabel("Time t / days")
ax.set_ylabel(r"Distance $r$ / $10^9$ m")
ax.set_xlim(left=0)
ax.set_ylim(0, 165)
ax.grid(True, alpha=0.3)
ax.legend(loc="lower left")

fig.tight_layout()
fig.savefig("earthsun.png")
plt.show()
