import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

st.set_page_config(page_title="Inventario Dulces", layout="wide")

# --- CONEXIÓN CLÁSICA ---
def conectar():
    # Define los permisos
    scopes = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
    
    # Carga las credenciales desde los Secretos de Streamlit
    creds = Credentials.from_service_account_info(
        st.secrets["connections"]["gsheets"]["service_account"],
        scopes=scopes
    )
    return gspread.authorize(creds)

# --- APP ---
try:
    st.title("🍬 Gestión de Inventario")
    
    # Conectamos
    client = conectar()
    
    # Abre la hoja usando la URL que está en secrets
    url = st.secrets["connections"]["gsheets"]["spreadsheet"]
    hoja = client.open_by_url(url).sheet1
    
    # Lee los datos
    data = hoja.get_all_records()
    df = pd.DataFrame(data)
    
    st.success("✅ Conectado correctamente")
    st.dataframe(df)

    # Formulario simple
    st.divider()
    with st.form("entrada"):
        nombre = st.text_input("Nombre del Dulce")
        cantidad = st.number_input("Cantidad", min_value=1)
        if st.form_submit_button("Guardar"):
            hoja.append_row([nombre, cantidad])
            st.success("Guardado")
            st.rerun()

except Exception as e:
    st.error("Hubo un error de conexión.")
    st.warning("Asegúrate de que en 'Secrets' la llave privada tenga comillas triples al principio y al final.")
    st.code(str(e))
