import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de la página
st.set_page_config(page_title="Dulces App", page_icon="🍬")
st.title("🍬 Gestión de Dulces (En la Nube)")

# --- URL DIRECTA DEL EXCEL (LA SOLUCIÓN BLINDADA) ---
URL_EXCEL = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit?usp=sharing"
# ----------------------------------------------------

# 2. Conexión
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para cargar datos
def cargar_datos():
    try:
        # Forzamos a leer desde la URL directa
        df = conn.read(spreadsheet=URL_EXCEL, worksheet="Hoja 1", usecols=[0, 1, 2, 3], ttl=5)
        df = df.dropna(how="all")
        return df
    except Exception as e:
        # Si falla, mostramos el error real para saber qué pasa
        st.error(f"Error detallado: {e}")
        return None

# Función para guardar datos
def guardar_datos(df):
    try:
        conn.update(spreadsheet=URL_EXCEL, worksheet="Hoja 1", data=df)
        st.success("¡Guardado en la nube! ☁️")
    except Exception as e:
        st.error(f"No se pudo guardar: {e}")

# 3. Lógica principal
df = cargar_datos()

if df is not None:
    st.success("✅ ¡Conexión Exitosa!")
    
    # Mostrar la tabla editable
    df_editado = st.data_editor(
        df,
        num_rows="dynamic",
        column_config={
            "Precio": st.column_config.NumberColumn(format="$%d"),
            "CantidadBodega": st.column_config.NumberColumn(min_value=0, step=1),
            "CantidadMochila": st.column_config.NumberColumn(min_value=0, step=1),
        },
        key="editor_dulces"
    )

    # Botón de guardar
    if st.button("💾 Guardar Cambios"):
        guardar_datos(df_editado)
        st.rerun()
else:
    st.warning("⚠️ No se pudo conectar. Verifica que borraste la caja de 'Secrets'.")


