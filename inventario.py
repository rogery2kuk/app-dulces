import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Dulces App", page_icon="🍬")
st.title("🍬 Gestión de Dulces (En la Nube)")

# --- CONEXIÓN A GOOGLE SHEETS (MODO SEGURO) ---
# Ponemos el enlace aquí directo para evitar errores de Secrets
url_fix = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit?usp=sharing"
conn = st.connection("gsheets", type=GSheetsConnection)

# Función para cargar datos
def cargar_datos():
    try:
        # Usamos url_fix para obligar a leer este archivo específico
        df = conn.read(spreadsheet=url_fix, worksheet="Hoja 1", usecols=[0, 1, 2, 3], ttl=5)
        df = df.dropna(how="all")
        return df
    except Exception as e:
        return None

# Función para guardar datos
def guardar_datos(df):
    try:
        # Usamos url_fix para obligar a guardar en este archivo específico
        conn.update(spreadsheet=url_fix, worksheet="Hoja 1", data=df)
    except:
        st.error("Error al guardar")
# Función para guardar datos
def guardar_datos(df):
    try:
        # Usamos url_fix para obligar a guardar en este archivo específico
        conn.update(spreadsheet=url_fix, worksheet="Hoja 1", data=df)
    except:
        st.error("Error al guardar")
    st.cache_data.clear()

# --- CARGAMOS LOS DATOS ---
df = cargar_datos()

if df is None:
    st.error("⚠️ Error de conexión: No se ha configurado el enlace al Excel en los 'Secrets' o la hoja no es pública.")
    st.stop()

if df.empty:
    df = pd.DataFrame(columns=["Dulce", "Precio", "CantidadBodega", "CantidadMochila"])

# --- PESTAÑAS ---
tab1, tab2, tab3 = st.tabs(["🏠 Bodega", "🎒 Mochila", "➕ Comprar"])

# --- PESTAÑA 1: BODEGA ---
with tab1:
    st.header("Inventario en Casa")
    if not df.empty:
        st.dataframe(df[["Dulce", "CantidadBodega", "Precio"]], use_container_width=True)
    else:
        st.info("No hay dulces todavía.")

# --- PESTAÑA 2: MOCHILA ---
with tab2:
    st.header("Gestión del Día")
    # Mostrar Mochila
    mochila = df[df["CantidadMochila"] > 0]
    if not mochila.empty:
        st.dataframe(mochila[["Dulce", "CantidadMochila", "Precio"]], use_container_width=True)
        total = (mochila["CantidadMochila"] * mochila["Precio"]).sum()
        st.success(f"💰 Venta esperada: ${total:,.0f}")
        
        if st.button("Vaciar Mochila (Fin del día)"):
            df["CantidadMochila"] = 0
            guardar_datos(df)
            st.rerun()
    else:
        st.info("Mochila vacía.")
    
    st.divider()
    
    # Mover a Mochila
    st.subheader("Sacar de Bodega")
    lista = df["Dulce"].unique().tolist()
    if lista:
        dulce = st.selectbox("Elige dulce:", lista)
        idx = df[df["Dulce"] == dulce].index[0]
        stock = df.at[idx, "CantidadBodega"]
        
        cant = st.number_input("Cantidad a llevar:", min_value=1, max_value=int(stock) if stock > 0 else 1)
        
        if st.button("Meter en mochila"):
            if stock >= cant:
                df.at[idx, "CantidadBodega"] -= cant
                df.at[idx, "CantidadMochila"] += cant
                guardar_datos(df)
                st.toast("¡Listo!", icon="✅")
                st.rerun()
            else:
                st.error("No hay suficientes.")

# --- PESTAÑA 3: NUEVO ---
with tab3:
    st.header("Registrar Compra")
    with st.form("nuevo"):
        nom = st.text_input("Nombre").strip().capitalize()
        pre = st.number_input("Precio", min_value=0.0)
        can = st.number_input("Cantidad", min_value=1)
        if st.form_submit_button("Guardar"):
            if nom:
                if nom in df["Dulce"].values:
                    idx = df[df["Dulce"] == nom].index[0]
                    df.at[idx, "CantidadBodega"] += can
                    df.at[idx, "Precio"] = pre
                else:
                    nuevo = pd.DataFrame([{"Dulce": nom, "Precio": pre, "CantidadBodega": can, "CantidadMochila": 0}])
                    df = pd.concat([df, nuevo], ignore_index=True)
                guardar_datos(df)
                st.success("Guardado.")
                st.rerun()


