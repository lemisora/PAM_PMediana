using JuMP, HiGHS, DelimitedFiles, SparseArrays

# Cargar la matriz de costos desde un archivo de texto
file_path = "matriz.txt"
cost_matrix = Float32.(readdlm(file_path))  # Leer archivo como matriz numérica

n = size(cost_matrix, 1)  # Número de ciudades
p = 9  # Número de hubs

# Convertir matriz a formato disperso si hay muchos ceros
cost_matrix_sparse = sparse(cost_matrix)

# Crear el modelo de optimización
model = Model(HiGHS.Optimizer)
# set_optimizer_attribute(model, "presolve", "on")   # Activar preprocesamiento (puede reducir memoria)
# set_optimizer_attribute(model, "threads", 12)       # Limitar número de hilos si tienes muchas variables
# set_optimizer_attribute(model, "primal_feasibility_tolerance", 1e-5)  # Menos restricciones en la solución
# set_optimizer_attribute(model, "dual_feasibility_tolerance", 1e-5)
# set_optimizer_attribute(model, "mip_rel_gap", 0.01)

# Variables binarias de asignación
@variable(model, x[1:n, 1:n], Bin)
# Variables binarias para los hubs
@variable(model, y[1:n], Bin)

# Función objetivo: minimizar el costo total de asignación
#@objective(model, Min, sum(x[i, j] * cost_matrix[i, j] for i in 1:n, j in 1:n))

# Función objetivo: minimizar el costo total de asignación
@objective(model, Min, sum(x[i, j] * cost_matrix_sparse[i, j] for i in 1:n, j in 1:n))


# Restricción: cada ciudad debe ser asignada a exactamente un hub
@constraint(model, [j in 1:n], sum(x[i, j] for i in 1:n) == 1)

# Restricción: exactamente p hubs deben estar abiertos
@constraint(model, sum(y[i] for i in 1:n) == p)

# Restricción: una ciudad solo puede ser asignada a un hub si ese hub está abierto
@constraint(model, [i in 1:n, j in 1:n], x[i, j] <= y[i])

# Resolver el problema
optimize!(model)

# Obtener y mostrar los resultados
println("Costo mínimo: ", objective_value(model))
println("Hubs seleccionados: ", [i for i in 1:n if value(y[i]) ≈ 1])
