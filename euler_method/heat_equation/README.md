# 1D Heat Equation – Explicit Euler (FTCS)

Mini project solving the one-dimensional heat equation

    ∂_t T(x,t) = α · ∂_x² T(x,t)

numerically with the **explicit Euler method** in time and a central second difference in space
(FTCS scheme: forward in time, centered in space). Two scripts visualize the result in different ways.

## Files

| File | Description |
|------|-------------|
| `heat_1d.py` | Live animation: the temperature profile is updated and redrawn after every time step. |
| `heat_1d_slider.py` | Computes all time steps first, then shows the result with a slider to browse through time. |

## Idea

Discretizing space with step `dx` and time with step `dt` gives the update rule

    u_i^{n+1} = u_i^n + α · dt / dx² · ( u_{i+1}^n - 2·u_i^n + u_{i-1}^n )

The initial condition `f(x)` is a smooth base profile with additional structure on top:

- `sin(πx)` as the base shape
- two sine waves (modes 5 and 17) as medium and fast oscillations
- three narrow Gaussian peaks at x = 0.2, 0.55 (negative) and 0.8

Heat diffusion damps the fast oscillations and sharp peaks first, while the smooth parts survive longest.
The profile therefore gets smoother and smoother over time.

## Usage

```bash
pip install numpy matplotlib
python heat_1d.py          # live animation
python heat_1d_slider.py   # precomputed result with slider
```

Both scripts need an interactive matplotlib backend (a window must be able to open).

### `heat_1d.py`

Redraws the profile after each step (with `plt.pause(0.01)`) and keeps the y-axis fixed at `[0, max(f)]`.
Closing the window stops the simulation. Since there are about 25,000 steps and every redraw pauses for at least 0.01 s,
a full run takes several minutes.

### `heat_1d_slider.py`

Runs the explicit Euler scheme for all steps (a few seconds), stores every profile and then opens a plot with a slider.
The slider is **logarithmic** (`log10(step+1)`), so you can inspect both the fast changes in the first steps and the slow
late-time behavior. The plot title shows the current time `t` and step index. Index 0 is the state after the first step.

## Parameters

| Variable | Meaning | Value |
|----------|---------|-------|
| `alpha` | Diffusion constant | 1.0 |
| `dx` | Spatial step | 0.01 |
| `dt` | Time step | `0.4 · dx² / alpha` = 4·10⁻⁵ |
| `x_vec` | Spatial grid | 0, 0.01, …, 0.99 (100 points) |
| `t_vec` | Time grid | 0 … 1 (about 25,000 steps) |

## Notes

- **Stability:** The explicit scheme is only stable for `α · dt / dx² ≤ 1/2`. With the chosen `dt` this ratio is 0.4,
  so the simulation is stable. A larger `dt` (ratio above 0.5) makes the solution blow up with growing oscillations.
- **Boundaries:** The first and last grid point are never updated, so they keep their initial values (fixed/Dirichlet boundary conditions).
- **Accuracy:** The scheme is first order in time and second order in space.
- In `heat_1d_slider.py` the list `u_vec_history_impl` is defined but unused, so only the explicit method is shown.