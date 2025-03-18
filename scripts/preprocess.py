def prepend_numbers_to_file(filename, max_number):
    # Crear la primera línea con los números
    numbers_line = " " + " ".join(map(str, range(1, max_number + 1))) + "\n"

    # Leer el contenido original del archivo y modificar cada fila
    with open(filename, "r") as f:
        content = f.readlines()

    # Añadir el número de fila en la primera columna de cada línea, comenzando desde 1
    updated_content = [f"{i+1} {line}" for i, line in enumerate(content)]

    # Escribir la nueva línea y el contenido actualizado en el archivo
    with open(filename, "w") as f:
        f.write(numbers_line)
        f.writelines(updated_content)


# Ejemplo de uso
filename = "matriz_PAM.txt"  # Reemplázalo con el nombre de tu archivo
max_number = 469  # Número máximo hasta el que quieres escribir
prepend_numbers_to_file(filename, max_number)
