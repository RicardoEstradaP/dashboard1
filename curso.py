import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import requests
from io import StringIO

# Cargar los datos desde el archivo CSV
@st.cache_data
def cargar_datos():
    url = "https://github.com/tu_usuario/tu_repositorio/raw/main/integridad.csv"  # Cambia esto con la URL correcta
    response = requests.get(url)
    
    if response.status_code != 200:
        st.error("Error al descargar el archivo CSV.")
        return pd.DataFrame()  # Retorna un DataFrame vacío si hay un error

    try:
        # Intentamos leer el archivo CSV con la codificación UTF-8 y delimitador por coma
        df = pd.read_csv(StringIO(response.text), encoding='utf-8', delimiter=',')
    except Exception as e:
        st.error(f"Error al leer el archivo CSV: {e}")
        return pd.DataFrame()  # Retorna un DataFrame vacío en caso de error
    
    return df

# Filtrar los datos según los valores seleccionados en los filtros
def filtrar_datos(uni_seleccionada, licenciatura_seleccionada, df):
    df_filtrado = df[(df['Universidad'] == uni_seleccionada) & 
                     (df['Licenciatura'] == licenciatura_seleccionada)]
    return df_filtrado

# Crear la gráfica
def crear_grafica(df_filtrado):
    if df_filtrado.empty:
        return None

    # Contar los valores de Integridad Académica
    integridad_count = df_filtrado['Integridad Académica'].value_counts()

    # Crear la gráfica de barras
    plt.figure(figsize=(10,6))
    integridad_count.plot(kind='bar', color='skyblue')
    plt.title('Integridad Académica por Licenciatura')
    plt.xlabel('Nivel de Integridad Académica')
    plt.ylabel('Cantidad de Estudiantes')

    # Guardar la gráfica como imagen
    grafica_path = '/tmp/grafica_integridad.png'
    plt.savefig(grafica_path)
    plt.close()
    
    return grafica_path

# Crear la interfaz de usuario en Streamlit
def app():
    # Cargar los datos
    df = cargar_datos()

    if df.empty:
        st.write("No se pudo cargar ningún dato.")
        return

    # Título del dashboard
    st.title('Dashboard de Integridad Académica')

    # Filtros de universidad
    universidades = df['Universidad'].unique()
    universidad_seleccionada = st.selectbox('Selecciona una universidad', universidades)

    # Filtrar según la universidad seleccionada
    df_filtrado_universidad = df[df['Universidad'] == universidad_seleccionada]

    # Filtros de licenciatura (dependiendo de la universidad seleccionada)
    licenciaturas = df_filtrado_universidad['Licenciatura'].unique()
    licenciatura_seleccionada = st.selectbox('Selecciona una licenciatura', licenciaturas)

    # Filtrar los datos según ambos filtros seleccionados
    df_filtrado = filtrar_datos(universidad_seleccionada, licenciatura_seleccionada, df)

    # Si hay datos filtrados, generar la gráfica
    if not df_filtrado.empty:
        # Crear la gráfica
        grafica_path = crear_grafica(df_filtrado)
        
        # Mostrar la gráfica
        st.image(grafica_path, caption='Gráfica de Integridad Académica', use_column_width=True)
        
        # Botón para descargar la gráfica
        with open(grafica_path, 'rb') as file:
            st.download_button(
                label="Descargar Gráfica",
                data=file,
                file_name="grafica_integridad.png",
                mime="image/png"
            )
    else:
        st.write('No hay datos para mostrar con los filtros seleccionados.')

if __name__ == "__main__":
    app()
