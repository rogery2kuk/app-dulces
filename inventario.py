import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

st.set_page_config(page_title="Inventario Dulces")
st.title("🍬 Gestión de Inventario")

# 1. Conexión simple y limpia
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # 2. Leemos los datos
    df = conn.read(ttl="0") # ttl=0 para que no guarde memoria vieja
    
    st.success("¡Conectado exitosamente!")
    st.dataframe(df)

    # 3. Formulario para guardar
    with st.form("nuevo_dulce"):
        nombre = st.text_input("Nombre del dulce")
        cantidad = st.number_input("Cantidad", min_value=1)
        boton = st.form_submit_button("Guardar")

        if boton and nombre:
            # SQL simple para insertar
            sql = f"INSERT INTO data (Nombre, Cantidad) VALUES ('{nombre}', {cantidad});"
            conn.sql(sql)
            st.success("Guardado. Actualiza la página si no lo ves.")
            
except Exception as e:
    st.error(f"Error de conexión: {e}")
