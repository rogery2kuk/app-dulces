import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuración básica
st.set_page_config(page_title="Dulces App", page_icon="🍬")
st.title("🍬 Gestión de Dulces (En la Nube)")

# 2. El enlace EXACTO (Sin espacios)
# Nota: He limpiado cualquier espacio oculto en esta linea
url_excel = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit?usp=sharing"

# 3. Conexión
try:
    conn = st.connection("gsheets", type=GSheetsConnection)

    # Cargar datos
    df = conn.read(spreadsheet=url_excel, worksheet="Hoja 1", usecols=[0, 1, 2, 3], ttl=5)
    df = df.dropna(how="all")

    # 4. Mostrar la app
    st.success("✅ ¡Conectado al Excel!")

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
        conn.update(spreadsheet=url_excel, worksheet="Hoja 1", data=df_editado)
        st.success("¡Guardado correctamente!")
        st.rerun()

except Exception as e:
    st.error("Hubo un error con el enlace o la conexión.")
    st.write(f"Detalle del error: {e}")
