import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# Configuración
st.set_page_config(page_title="Dulces App", page_icon="🍬")
st.title("🍬 Gestión de Dulces (En la Nube)")

# --- TU ENLACE (Ya lo puse yo, no lo toques) ---
url_excel = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit?usp=sharing"
# -----------------------------------------------

# Conexión
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Cargar datos (Sin cache para que actualice rápido)
    df = conn.read(spreadsheet=url_excel, worksheet="Hoja 1", usecols=[0, 1, 2, 3], ttl=0)
    df = df.dropna(how="all")

    st.success("✅ ¡Conexión Exitosa!")

    # Tabla editable
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

    # Botón guardar
    if st.button("💾 Guardar Cambios"):
        try:
            conn.update(spreadsheet=url_excel, worksheet="Hoja 1", data=df_editado)
            st.success("¡Guardado en Google Sheets! ☁️")
        except Exception as e:
            st.error(f"Error al guardar: {e}")

except Exception as e:
    st.error("Hubo un error de conexión.")
    st.write(e)
