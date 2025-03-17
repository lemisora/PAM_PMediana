import pandas as pd

# Cargar el archivo de Excel
archivo_excel = "tmtoluca.xlsx"  # Reemplaza con el nombre de tu archivo
hoja = "Hoja1"  # Reemplaza con el nombre de la hoja si es necesario

# Leer el archivo de Excel
df = pd.read_excel(archivo_excel, sheet_name=hoja, engine="openpyxl")

# Guardar en CSV
archivo_csv = "matriz.csv"
df.to_csv(archivo_csv, index=False)  # `index=False` evita que agregue una columna de índices

print(f"Archivo convertido y guardado como {archivo_csv}")
