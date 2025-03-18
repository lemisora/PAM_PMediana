using JuMP, Cbc, DelimitedFiles

# Ruta al archivo de costos
ruta_archivo = "matriz.csv"

# Leer la matriz desde el archivo
costo = readdlm(ruta_archivo, Float32)

# Verificar la matriz leída
println("Matriz de costos leída:")
println(costo)

# Crear el modelo
model = Model(Cbc.Optimizer)

set_optimizer_attribute(model, "preprocess", "aggressive")
# Ajustar parámetros de CBC
set_optimizer_attribute(model, "seconds", 600)  # Límite de tiempo de 600 segundos
set_optimizer_attribute(model, "gap", 0.01)    # Tolerancia de gap del 1%
set_optimizer_attribute(model, "logLevel", 1)  # Nivel de logging (1 para ver detalles)

# Conjuntos
cities = 1:369
hubs = 1:369

# Variables
@variable(model, x[i in cities, j in cities], Bin)  # Asignación
@variable(model, y[i in hubs], Bin)                # Selección de hubs

# Función objetivo (minimizar el costo total)
@objective(model, Min, sum(x[i, j] * costo[i, j] for i in cities, j in cities))

# Restricciones
for j in cities
    @constraint(model, sum(x[i, j] for i in cities) == 1)  # Cada ciudad debe asignarse a un hub
end

@constraint(model, sum(y[i] for i in hubs) == 20)           # Seleccionar exactamente 20 hubs

for i in cities
    @constraint(model, sum(x[i, j] for j in cities) <= 369 * y[i])  # Restricción de activación
end

# Resolver el problema
optimize!(model)

# Resultados
println("Status: ", termination_status(model))
println("Costo mínimo: ", objective_value(model))

# Mostrar los hubs seleccionados
println("Hubs seleccionados:")
for i in hubs
    if value(y[i]) == 1
        println("Hub ", i)
    end
end
