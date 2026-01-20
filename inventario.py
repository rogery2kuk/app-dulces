import streamlit as st
import json
import os
import pandas as pd

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Mi Tienda de Dulces", page_icon="🍬")

ARCHIVO_DATOS = "mis_dulces_web.json"

# --- FUNCIONES DE DATOS ---
def cargar_datos():
    if os.path.exists(ARCHIVO_DATOS):
        try:
            with open(ARCHIVO_DATOS, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return {"bodega": {}, "mochila": {}}
    return {"bodega": {}, "mochila": {}}

def guardar_datos(datos):
    with open(ARCHIVO_DATOS, "w", encoding='utf-8') as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)

# Cargar datos al inicio
datos = cargar_datos()

# --- INTERFAZ GRÁFICA (LO QUE SE VE EN LA WEB) ---
st.title("🍬 Gestión de Dulces Escolar")

# Creamos pestañas para organizar la web
tab1, tab2, tab3 = st.tabs(["🏠 Bodega (Casa)", "🎒 Mochila (Colegio)", "➕ Agregar Nuevo"])

# --- PESTAÑA 1: LA BODEGA ---
with tab1:
    st.header("Inventario en Casa")
    
    if not datos["bodega"]:
        st.info("Tu bodega está vacía. Ve a la pestaña 'Agregar Nuevo'.")
    else:
        # Convertimos los datos a una tabla bonita
        lista_bodega = []
        for nombre, info in datos["bodega"].items():
            lista_bodega.append({
                "Dulce": nombre,
                "Cantidad": info["cantidad"],
                "Precio": f"${info['precio']}"
            })
        st.dataframe(pd.DataFrame(lista_bodega), use_container_width=True)

# --- PESTAÑA 2: LA MOCHILA ---
with tab2:
    st.header("¿Qué llevas hoy?")
    
    # SECCIÓN 1: VER LO QUE YA TIENES EN LA MOCHILA
    st.subheader("🎒 En tu mochila ahora:")
    if datos["mochila"]:
        total_esperado = 0
        lista_mochila = []
        for nombre, info in datos["mochila"].items():
            subtotal = info['cantidad'] * info['precio']
            total_esperado += subtotal
            lista_mochila.append({
                "Dulce": nombre,
                "Llevas": info["cantidad"],
                "Venta Esperada": f"${subtotal}"
            })
        st.table(pd.DataFrame(lista_mochila))
        st.success(f"💰 Ganancia total posible hoy: ${total_esperado}")
        
        if st.button("🔄 Vaciar Mochila (Fin del día)"):
            datos["mochila"] = {}
            guardar_datos(datos)
            st.rerun()
    else:
        st.warning("La mochila está vacía.")

    st.divider()

    # SECCIÓN 2: MOVER DE BODEGA A MOCHILA
    st.subheader("move de Bodega ➡️ Mochila")
    
    opciones_dulces = list(datos["bodega"].keys())
    
    if opciones_dulces:
        col1, col2 = st.columns(2)
        with col1:
            dulce_seleccionado = st.selectbox("Elige el dulce", opciones_dulces)
        
        stock_actual = datos["bodega"][dulce_seleccionado]["cantidad"]
        precio_actual = datos["bodega"][dulce_seleccionado]["precio"]
        
        with col2:
            cantidad_mover = st.number_input(f"Cantidad (Max: {stock_actual})", 
                                           min_value=1, max_value=stock_actual if stock_actual > 0 else 1)

        if st.button("Meter a la mochila"):
            if stock_actual >= cantidad_mover:
                # Restar de bodega
                datos["bodega"][dulce_seleccionado]["cantidad"] -= cantidad_mover
                
                # Sumar a mochila
                if dulce_seleccionado in datos["mochila"]:
                    datos["mochila"][dulce_seleccionado]["cantidad"] += cantidad_mover
                else:
                    datos["mochila"][dulce_seleccionado] = {
                        "cantidad": cantidad_mover, 
                        "precio": precio_actual
                    }
                
                guardar_datos(datos)
                st.toast(f"¡Agregaste {cantidad_mover} {dulce_seleccionado}!", icon="✅")
                st.rerun() # Recarga la página para ver cambios
            else:
                st.error("No tienes suficientes dulces en casa.")
    else:
        st.write("No hay dulces en bodega para mover.")

# --- PESTAÑA 3: AGREGAR ---
with tab3:
    st.header("Comprar / Agregar Stock")
    
    with st.form("nuevo_dulce"):
        nuevo_nombre = st.text_input("Nombre del dulce").strip().capitalize()
        nueva_cantidad = st.number_input("Cantidad comprada", min_value=1)
        nuevo_precio = st.number_input("Precio de venta", min_value=50.0)
        
        enviado = st.form_submit_button("Guardar en Bodega")
        
        if enviado:
            if nuevo_nombre:
                datos["bodega"][nuevo_nombre] = {
                    "cantidad": nueva_cantidad,
                    "precio": nuevo_precio
                }
                guardar_datos(datos)
                st.success(f"{nuevo_nombre} guardado correctamente.")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Escribe un nombre.")
