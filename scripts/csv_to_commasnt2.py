import csv

# Ruta del archivo CSV original
input_csv_file = 'matriz.csv'

# Ruta del archivo de salida (formato Lingo)
output_txt_file = 'matriz2.txt'

# Abrir el archivo CSV original y el archivo de salida
with open(input_csv_file, 'r', newline='') as csvfile, open(output_txt_file, 'w') as txtfile:
    # Leer el archivo CSV
    csv_reader = csv.reader(csvfile)

    # Escribir los valores en un solo bloque, separados por espacios
    for row in csv_reader:
        # Convertir la fila a una cadena con espacios en lugar de comas
        row_with_spaces = ' '.join(row)
        # Escribir la fila en el archivo de texto
        txtfile.write(row_with_spaces + ' ')

    # Asegurarse de que el archivo termine con un salto de línea
    txtfile.write('\n')

print(f"Archivo convertido y guardado en: {output_txt_file}")
