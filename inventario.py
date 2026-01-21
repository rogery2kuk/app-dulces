import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuración de página
st.set_page_config(page_title="Dulces App", page_icon="🍬")
st.title("🍬 Gestión de Dulces (En la Nube)")

# 2. Enlace DIRECTO (Sin espacios)
url_excel = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit?usp=sharing"

# 3. Conexión y Carga
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # Leer datos
    df = conn.read(spreadsheet=url_excel, worksheet="Hoja 1", usecols=[0, 1, 2, 3], ttl=5)
    df = df.dropna(how="all")

    st.success("✅ ¡Conectado correctamente!")

    # 4. Tabla Editable
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

    # 5. Botón Guardar
    if st.button("💾 Guardar Cambios"):
        conn.update(spreadsheet=url_excel, worksheet="Hoja 1", data=df_editado)
        st.success("¡Cambios guardados en la nube!")
        st.rerun()

except Exception as e:
    st.error("Error de conexión. Verifica que el enlace no tenga espacios.")
    st.write(e)

