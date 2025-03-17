import sys

def remove_last_line_and_column(filename, iterations):
    for _ in range(iterations):
        # Leer el contenido original del archivo
        with open(filename, "r") as f:
            lines = f.readlines()

        # Si el archivo no tiene suficientes líneas, no hacer nada
        if not lines:
            return

        # Eliminar la última línea
        lines = lines[:-1]

        # Procesar cada línea eliminando la última columna
        new_lines = []
        for line in lines:
            parts = line.strip().split()
            if parts:
                new_lines.append(" ".join(parts[:-1]) + "\n")

        # Escribir el nuevo contenido en el archivo
        with open(filename, "w") as f:
            f.writelines(new_lines)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <nombre_del_archivo> <numero_de_iteraciones>")
        sys.exit(1)

    filename = sys.argv[1]
    iterations = int(sys.argv[2])
    remove_last_line_and_column(filename, iterations)
