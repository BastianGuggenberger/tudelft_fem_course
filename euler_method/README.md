# Euler Method

Visualizations and implementations of the Euler methods (explicit and implicit) that I learned in the ATHENS course.

## Projects

### `earth_sun`
Demonstration of the **explicit Euler method** on a physical example: the Earth is suddenly stopped in its orbit
and falls radially into the Sun. The simulated fall time (≈ 64.6 days) is compared with the analytical result.

### `heat_equation`
Numerical solution of the **1D heat equation** with the explicit Euler method (FTCS scheme).
Contains a live animation and a version with a logarithmic time slider to browse through the whole simulation.

### `euler_comparison`
Comparison of the **implicit and explicit Euler method** on the simple ODE `f'(x) = a·f(x)` against the exact solution.
Shows how the explicit method underestimates and the implicit method overestimates the exponential growth.

## Requirements

```bash
pip install numpy matplotlib
```