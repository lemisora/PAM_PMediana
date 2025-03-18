using JuMP, GLPK, DelimitedFiles, BenchmarkTools

# Cargar la matriz de costos desde un archivo CSV
file_path = "matriz.txt"
cost_matrix = Float32.(readdlm(file_path))  # Asegurar tipo Float32

n = size(cost_matrix, 1)  # Número de ciudades (369)
p = 20  # Número de hubs

# Crear el modelo de optimización con GLPK
model = Model(GLPK.Optimizer)

# Variables binarias de asignación
@variable(model, x[1:n, 1:n], Bin)
# Variables binarias para los hubs
@variable(model, y[1:n], Bin)

# Función objetivo: minimizar el costo total de asignación
@objective(model, Min, sum(x[i, j] * cost_matrix[i, j] for i in 1:n, j in 1:n))

# Restricción: cada ciudad debe ser asignada a exactamente un hub
@constraint(model, [j in 1:n], sum(x[i, j] for i in 1:n) == 1)

# Restricción: exactamente p hubs deben estar abiertos
@constraint(model, sum(y[i] for i in 1:n) == p)

# Restricción: una ciudad solo puede ser asignada a un hub si ese hub está abierto
@constraint(model, [i in 1:n, j in 1:n], x[i, j] <= y[i])

# Resolver el problema con GLPK
# Medir tiempo de ejecución
start_time = time()
optimize!(model)
end_time = time()
elapsed_time = end_time - start_time

# Mostrar resultados
println("Tiempo de ejecución: ", round(elapsed_time, digits=4), " segundos")
println("Costo mínimo: ", objective_value(model))
println("Hubs seleccionados: ", [i for i in 1:n if value(y[i]) ≈ 1])
