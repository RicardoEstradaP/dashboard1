import pandas as pd
import matplotlib.pyplot as plt
import os
import seaborn as sns  # Para mejorar la paleta de colores
import matplotlib.colors as mcolors
import numpy as np

# Ruta del archivo en tu Mac
archivo = "/Users/ricardoestrada/Archivos Python/curso/prueba.xlsx"

# Cargar datos
df = pd.read_excel(archivo)

# Calcular el promedio de cada caso (fila), considerando solo las columnas B a E
df["Promedio Caso"] = df.iloc[:, 1:5].mean(axis=1)

# Calcular el promedio final de cada institución (promedio de los casos)
promedio_por_institucion = df.groupby(df.columns[0])["Promedio Caso"].mean().reset_index()
promedio_por_institucion.rename(columns={"Promedio Caso": "Promedio Final Institución"}, inplace=True)

# Calcular el promedio de cada pregunta por institución
promedio_preguntas = df.groupby(df.columns[0]).mean(numeric_only=True).reset_index()

# Unir ambos resultados en un solo DataFrame
resultado_final = pd.merge(promedio_preguntas, promedio_por_institucion, on=df.columns[0])

# Definir la ruta de salida en el escritorio
ruta_csv = os.path.expanduser("~/Desktop/promedios_instituciones.csv")

# Guardar como CSV
resultado_final.to_csv(ruta_csv, index=False, encoding="utf-8")

# 📊 Gráfico de barras del promedio final por institución (ordenado de menor a mayor)
promedio_por_institucion = promedio_por_institucion.sort_values(by="Promedio Final Institución")

# Crear un mapa de colores personalizado en degradado azul
cmap = mcolors.LinearSegmentedColormap.from_list("degradado_azul", ["#ffffff", "#192E4C"])

# Obtener una secuencia de colores del mapa de colores
n_barras = len(promedio_por_institucion)
colores = [cmap(i / n_barras) for i in range(n_barras)]

# Calcular el promedio general
promedio_general = promedio_por_institucion["Promedio Final Institución"].mean()

plt.figure(figsize=(10, 6))
barplot = sns.barplot(
    x="Promedio Final Institución",
    y=promedio_por_institucion[df.columns[0]],
    data=promedio_por_institucion,
    palette=colores  # Usar los colores del degradado
)

# Agregar una línea punteada para el promedio general
plt.axvline(promedio_general, color="#C89211", linestyle="--", linewidth=2, label=f"Promedio General: {promedio_general:.2f}")

# Personalizar etiquetas y título
plt.xlabel("Promedio Final")
plt.ylabel("Instituciones")
plt.title("Promedio Final por Institución (Ordenado)")
plt.grid(axis="x", linestyle="--", alpha=0.7)

# Mostrar leyenda
plt.legend()

# Definir la ruta para guardar el gráfico
ruta_grafico = os.path.expanduser("~/Desktop/promedio_instituciones.png")
plt.savefig(ruta_grafico, bbox_inches="tight")

# Mostrar gráfico
plt.show()

print(f"Archivo CSV guardado en: {ruta_csv}")
print(f"Gráfico guardado en: {ruta_grafico}")
