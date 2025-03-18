import pandas as pd

# Cargar el archivo de Excel sin encabezados
archivo_excel = "tmtoluca.xlsx"  # Reemplaza con el nombre de tu archivo
hoja = "Hoja1"  # Reemplaza con el nombre de la hoja si es necesario

# Leer el archivo de Excel
df = pd.read_excel(archivo_excel, sheet_name=hoja, header=None, engine="openpyxl")

# Guardar en CSV asegurando formato correcto
archivo_csv = "matriz.txt"
df.to_csv(archivo_csv, sep=" ", index=False, header=False, float_format="%.4f")

print(f"Archivo convertido y guardado como {archivo_csv}")
