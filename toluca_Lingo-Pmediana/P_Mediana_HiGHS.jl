using JuMP, HiGHS, DelimitedFiles, SparseArrays

# Cargar la matriz de costos desde un archivo de texto
file_path = "matriz.txt"
cost_matrix = Float32.(readdlm(file_path))  # Leer archivo como matriz numérica

n = size(cost_matrix, 1)  # Número de ciudades
p = 63  # Número de hubs

# Convertir matriz a formato disperso si hay muchos ceros
cost_matrix_sparse = sparse(cost_matrix)

# Crear el modelo de optimización
model = Model(HiGHS.Optimizer)
#set_optimizer_attribute(model, "presolve", "on")   # Activar preprocesamiento (puede reducir memoria)
#set_optimizer_attribute(model, "threads", 12)       # Limitar número de hilos si tienes muchas variables
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

# Medir el tiempo de la optimización
println("Optimizando el modelo con HiGHS...")
tiempo_calculo_elapsed = @elapsed begin
    optimize!(model)
end

# Mostrar resultados
println("\n--- Resultados HiGHS ---")
if termination_status(model) == MOI.OPTIMAL || termination_status(model) == MOI.LOCALLY_SOLVED || termination_status(model) == MOI.TIME_LIMIT
    println("Estado de terminación: ", termination_status(model))
    println("Costo mínimo: ", objective_value(model))

    hubs_seleccionados = [i for i in 1:n if value(y[i]) ≈ 1.0]
    println("Hubs seleccionados (", length(hubs_seleccionados), "): ", hubs_seleccionados)
else
    println("El problema no se resolvió a optimalidad o dentro del límite de tiempo.")
    println("Estado de terminación: ", termination_status(model))
end

println("\n--- Tiempos de Ejecución HiGHS ---")
println("Tiempo de 'optimize!' medido con @elapsed: ", round(tiempo_calculo_elapsed, digits=4), " segundos.")
println("Tiempo de solución reportado por JuMP (solve_time): ", round(solve_time(model), digits=4), " segundos.")
println("--------------------------------------\n")
