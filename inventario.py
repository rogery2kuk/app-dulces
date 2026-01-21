import streamlit as st
import pandas as pd
from streamlit_gsheets import GSheetsConnection

# 1. Configuración
st.set_page_config(page_title="Dulces App", page_icon="🍬")
st.title("🍬 Gestión de Dulces (En la Nube)")

# URL DEL EXCEL
url_excel = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit?usp=sharing"

# 2. Conexión
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    
    # --- EL CAMBIO MAGICO ESTA AQUI ---
    # Cambiamos worksheet="Hoja 1" por worksheet=0
    # El 0 significa "La primera hoja", sin importar cómo se llame.
    df = conn.read(spreadsheet=url_excel, worksheet=0, usecols=[0, 1, 2, 3], ttl=0)
    
    # Limpieza básica
    df = df.dropna(how="all")

    st.success("✅ ¡Conectado sin errores de espacio!")

    # 3. Tabla Editable
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

    # 4. Botón Guardar
    if st.button("💾 Guardar Cambios"):
        try:
            # Aquí también usamos 0 para guardar en la primera hoja
            conn.update(spreadsheet=url_excel, worksheet=0, data=df_editado)
            st.success("¡Guardado exitoso! ☁️")
            st.rerun()
        except Exception as e:
            st.error(f"Error al guardar: {e}")

except Exception as e:
    st.error("Ocurrió un error. Detalles abajo:")
    st.code(e) # Esto nos mostrará el error limpio si pasa algo más
