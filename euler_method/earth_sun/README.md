# Earth Falling into the Sun – Explicit Euler Method

Mini project demonstrating the **explicit Euler method** on a physical example:
the Earth is suddenly stopped (v = 0 at 1 AU) and falls radially into the Sun.

## Idea

The equation of motion for radial free fall is

    r'' = -G·M / r²

The script solves it numerically with the explicit Euler method (time step dt = 1 h):

    v_{n+1} = v_n - G·M / r_n² · dt
    r_{n+1} = r_n + v_{n+1} · dt

The simulation runs until r ≤ 0 and prints the estimated fall time.
For comparison, the analytical fall time

    t = π/2 · sqrt( r₀³ / (2·G·M) ) ≈ 64.6 days

is computed and drawn in the plot as a dashed line.

## Usage

```bash
pip install numpy matplotlib
python earth_sun.py
```

Output: fall time (Euler vs. analytical) in the console and the plot `earthsun.png`.

## Parameters

| Variable | Meaning | Value |
|----------|---------|-------|
| `dt` | Time step | 3600 s |
| `r` | Initial distance | 1.496·10¹¹ m (1 AU) |
| `v` | Initial velocity | 0 m/s |
| `mG` | G · M_Sun | ≈ 1.326·10²⁰ m³/s² |

## Notes

- The explicit Euler method is only first-order accurate; a smaller `dt` improves the result.
- As r → 0 the force (1/r²) diverges, so the simulation becomes inaccurate there – the stopping criterion `r > 0` is deliberately kept simple.