#1d finite element method example in julia

using LinearAlgebra
using Plots

alpha = 0.0

f(x) = x^2

plot()   # empty plot
for k in 1:10
    N = 2*k
    x_vec = range(0, 1, length=N+1)

    f_vec = zeros(N+1)
    for i in 1:N
        h = x_vec[i+1] - x_vec[i]
        f_vec[i]   += h/2 * f(x_vec[i])
        f_vec[i+1] += h/2 * f(x_vec[i+1])
    end

    A = zeros(N+1, N+1)
    for i in 1:N
        factor = 1 / (x_vec[i+1] - x_vec[i])
        A[i,i]     += factor
        A[i+1,i+1] += factor
        A[i,i+1]   -= factor
        A[i+1,i]   -= factor
    end

    # Dirichlet Boundary Conditions
    A[1,:] .= 0.0
    A[1,1] = 1.0
    f_vec[1] = alpha

    c = A \ f_vec

    plot!(x_vec, c, label="N = $N")
end


plot!(title = "1D-FEM: Convergence of the Solution", xlabel = "x", ylabel = "u(x)", legend = :topleft, grid = true, gridalpha = 0.25, framestyle = :box, size = (900, 600), dpi = 300, linewidth = 2.5, palette = :viridis, titlefontsize = 16, guidefontsize = 13, tickfontsize = 11, legendfontsize = 10, background_color_legend = RGBA(1, 1, 1, 0.8), left_margin = 5Plots.mm, bottom_margin = 5Plots.mm)
savefig("fem_1d_julia.png")