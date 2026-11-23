# Implicit vs. Explicit Euler Method

Mini project comparing the **explicit** and **implicit Euler method** on the simple linear ODE

    f'(x) = a · f(x),   f(0) = 1

whose exact solution is `f(x) = exp(a·x)`.

## Idea

With time step `dt`, the two methods read

    explicit:  u_{k+1} = u_k + dt · a · u_k      =  (1 + a·dt) · u_k
    implicit:  u_{k+1} = u_k + dt · a · u_{k+1}  =  u_k / (1 - a·dt)

Both are first-order accurate. For `a > 0` (exponential growth) the explicit method
**underestimates** and the implicit method **overestimates** the exact solution,
so the exact curve lies between the two.

## Usage

```bash
pip install numpy matplotlib
python euler.py
```

Output: the plot `plot.png` (exact solution, implicit and explicit Euler).

## Parameters

| Variable | Meaning | Value |
|----------|---------|-------|
| `a` | Growth rate in the ODE | 1.0 |
| `dt` | Time step | 0.1 |
| `ts` | Time grid | 0, 0.1, …, 0.9 |

## Notes

- A smaller `dt` brings both numerical solutions closer to the exact one.
- For `a < 0` (decay) the implicit method stays stable for any `dt`, while the explicit method becomes unstable for `dt > 2/|a|`.