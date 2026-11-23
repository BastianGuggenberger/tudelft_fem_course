
#---------------------------------------------------------------------------
#-------------------------- 1. meshing
#---------------------------------------------------------------------------

using Gmsh: gmsh

gmsh.initialize()
gmsh.model.add("rectangle")

# Target element size (approx. edge length of the triangles)
lc = 0.1

# 4 corner points: addPoint(x, y, z, lc, tag)
gmsh.model.geo.addPoint(0, 0, 0, lc, 1)   # bottom left
gmsh.model.geo.addPoint(2, 0, 0, lc, 2)   # bottom right
gmsh.model.geo.addPoint(2, 2, 0, lc, 3)   # top right
gmsh.model.geo.addPoint(0, 2, 0, lc, 4)   # top left

# 4 lines: addLine(start point, end point, tag)
# Going counter-clockwise: 1 -> 2 -> 3 -> 4 -> 1
gmsh.model.geo.addLine(1, 2, 1)
gmsh.model.geo.addLine(2, 3, 2)
gmsh.model.geo.addLine(3, 4, 3)
gmsh.model.geo.addLine(4, 1, 4)

# Closed loop from the 4 lines: addCurveLoop([line tags], tag)
gmsh.model.geo.addCurveLoop([1, 2, 3, 4], 1)

# Surface filled by the loop (this is what gets meshed): addPlaneSurface([loop tags], tag)
gmsh.model.geo.addPlaneSurface([1], 1)

# Hand the geometry over to Gmsh (required before meshing)
gmsh.model.geo.synchronize()

# Generate the 2D mesh and save it
gmsh.model.mesh.generate(2)

# Get all mesh nodes: tags and coordinates
node_tags, coords, _ = gmsh.model.mesh.getNodes()

# coords is one flat vector: [x1, y1, z1, x2, y2, z2, ...]
# Pick every 3rd entry to separate x and y (z is always 0 in 2D)
x = coords[1:3:end]
y = coords[2:3:end]

# Sort by node tag so that x[i], y[i] belong to node number i
order = sortperm(node_tags)
x = x[order]
y = y[order]
nnodes = length(x)

# Get all 2D elements of surface 1: types, element tags, node tags
elem_types, elem_tags, elem_node_tags = gmsh.model.mesh.getElements(2, 1)

# Flat vector [n1,n2,n3, n1,n2,n3, ...] -> matrix with 3 rows
# Column e holds the 3 node numbers of element e
conn = reshape(elem_node_tags[1], 3, :)
nel = size(conn, 2)

# List of elements, each as ((x1,y1,i), (x2,y2,j), (x3,y3,k))
elements = [((x[conn[1,e]], y[conn[1,e]], conn[1,e]),
             (x[conn[2,e]], y[conn[2,e]], conn[2,e]),
             (x[conn[3,e]], y[conn[3,e]], conn[3,e])) for e in 1:nel]


println("Number of nodes: ", nnodes)
println("Number of elements: ", nel)

#----------------------------------------------------------------------------------
#------------------------------- 2. FEM 
#----------------------------------------------------------------------------------

using LinearAlgebra
using Plots

alpha = 0.0

f(x,y) = x^3 + y^3

plot()   # leere Abbildung anlegen


f_vec = zeros(nnodes)
A = zeros(nnodes,nnodes)

for i in 1:nel

    element = elements[i]
    (x1, y1, a), (x2, y2, b), (x3, y3, c) = element
    surface = 1/2 * abs((x2 - x1)*(y3 - y1) - (x3 - x1)*(y2 - y1))
    center = (1/3 * (x1+x2+x3), 1/3 * (y1+y2+y3))
    fek = 1/3 * surface * f(center[1],center[2])

    f_vec[a]   += fek
    f_vec[b]   += fek
    f_vec[c]   += fek

    #local element stiffness matrix
    b1 = y2 - y3
    b2 = y3 - y1
    b3 = y1 - y2
    d1 = x3 - x2
    d2 = x1 - x3
    d3 = x2 - x1

    A_local = zeros(3,3)
    A_local[1,1] = (b1*b1 + d1*d1) / (4*surface)
    A_local[1,2] = (b1*b2 + d1*d2) / (4*surface)
    A_local[1,3] = (b1*b3 + d1*d3) / (4*surface)
    A_local[2,1] = (b2*b1 + d2*d1) / (4*surface)
    A_local[2,2] = (b2*b2 + d2*d2) / (4*surface)
    A_local[2,3] = (b2*b3 + d2*d3) / (4*surface)
    A_local[3,1] = (b3*b1 + d3*d1) / (4*surface)
    A_local[3,2] = (b3*b2 + d3*d2) / (4*surface)
    A_local[3,3] = (b3*b3 + d3*d3) / (4*surface)

    for m in 1:3
        for n in 1:3
            A[element[m][3],element[n][3]] += A_local[m,n]
        end
    end

end

# Dirichlet on the left boundary

nodes_boundary = []
for i in 1:nnodes
    if x[i]==0
        push!(nodes_boundary,i)
    end
end

for i in nodes_boundary
    for j in 1:nnodes
        if (j!=i)
            A[i,j]=0
        else
            A[i,j]=1
        end
    end
    f_vec[i]=0.0
end


u = A \ f_vec



scatter(x, y,
    zcolor = u,
    color = :viridis,
    markershape = :square,
    markersize = 6,
    markerstrokewidth = 0,
    aspect_ratio = :equal,
    label = "",
    title = "2D-FEM: Solution u(x,y)",
    xlabel = "x",
    ylabel = "y",
    colorbar_title = "u(x,y)",
    framestyle = :box,
    grid = false,
    xlims = (0, 2),
    ylims = (0, 2),
    size = (800, 700),
    dpi = 300,
    titlefontsize = 16,
    guidefontsize = 13,
    tickfontsize = 11,
    left_margin = 5Plots.mm,
    bottom_margin = 5Plots.mm)
savefig("fem_2d_julia.png")