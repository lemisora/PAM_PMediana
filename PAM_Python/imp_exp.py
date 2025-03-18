class ImpExp:
    def __init__(self):
        self.d = None  # Matriz de disimilitud
        self.nameObjects = None  # Nombres de los objetos
        self.nObjects = 0  # Número de objetos
        self.nVariables = 0  # Número de variables

    # Importa la matriz de costos desde un archivo
    def importMatrixCost(self, fileName):
        with open(fileName, 'r') as file:
            lines = file.readlines()
            self.nObjects = len(lines) - 1
            self.nVariables = self.nObjects
            self.nameObjects = [''] * self.nObjects
            self.d = [[0.0 for _ in range(self.nObjects)] for _ in range(self.nObjects)]

            # Saltar la primera línea (encabezado)
            for i in range(self.nObjects):
                line = lines[i + 1].strip()
                if not line:
                    raise IOError(f"Línea vacía en el archivo en la posición {i + 1}")
                parts = line.split()
                self.nameObjects[i] = parts[0]
                for j in range(self.nObjects):
                    if len(parts) <= j + 1 or not parts[j + 1].strip():
                        raise IOError(
                            f"Valor faltante en la matriz en la fila {i + 1}, columna {j + 1}")
                    self.d[i][j] = float(parts[j + 1])

    # Obtiene el número de filas en un archivo
    def getNRows(self, fileName):
        with open(fileName, 'r') as file:
            return sum(1 for _ in file)
