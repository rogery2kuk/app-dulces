import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="Inventario Dulces", layout="wide")

# --- CREDENCIALES INTEGRADAS ---
def obtener_conexion():
    scope = ['https://www.googleapis.com/auth/spreadsheets', 'https://www.googleapis.com/auth/drive']
    
    # Tu llave privada tal cual
    clave_privada = "-----BEGIN PRIVATE KEY-----\nMIIEvQIBADANBgkqhkiG9w0BAQEFAASCBKcwggSjAgEAAoIBAQDVcZYOgZvOLgbX\nOBVdatmDToEwEOubhV/qDuC8O8quY+zDVlAzGzGoO7fCqpz0GsYWDHDfDlJNqgeZ\nISEP7C9yLOYhNGjd/DBpRseZNTt3E8iyzien0HHapEMm1rj4OwOfr3qt3ossIMAs\n6NN22NbkCx1LmMet8pXaPRtqgqlVcj95XSGRlOud6Fd7C2YjznJ8tVcTP/Env/J1\nShsD/t2KSlLZlbCoklhX5IcMQ3wSkoDnsJj323caC7cSZnSGEXFDWUGYIKnWH/rU\nb5kbAD1utO29T8bg0FHJBYRxd9JwKnixVC/dLPLPbqy9gYxfohbmuwbjNzPML2JE\ndeGXXmmrAgMBAAECggEAVbQtJ5f9QrWSg5p+YatEuYetMeqpYCIW2DmvHYX4pTt0\nVx7yRwMVVlLcP2sYaJ/TiAjozXfHrm2mbWMzDlys1HCY2x5bOT9JBQypmqgYP4EP\nJlTG8YguHzezywWO8gVoOBdS8DuasFZaM+4s8tywtJKN6cvn6b2tVBsTRho++hKQ\nd9gdR2A1BplwmanPQFoYlOvICgy4tMZVXJ2nRdI0WvOIxOpAbaeiG5JihQ2bkrXn\nBqGQ22njQQKcbwTpTjL74IcSZAg//ogj1yPZ/ePzpGgFeteREa4JRjcRxvCCWaGR\nwmw9u8NGU9KebZbgEYO3eURGe6wz5F5HeRo0E9a8iQKBgQD9ltb+r6AOmda+fXXQ\nDFc/+XDwly78bPYuUNz3kEEj3QALQFpAgnAzNMPX5uIZ7nsee8tK9q3u5UrbAvig\nTjJKX5596ND+MsIxFm7mFviG1ll/o/I8dpeZWbEZCsQQLOYN0alwQKGcJTNKHmxh\nKREAH6s7JUEAP2NptvC6kFtkHwKBgQDXeQtOPyEdCid0hKhc28n038ebLzcN6U72\n8aT9XHnjYW4VH7JJCEvNzemrdub51MWe6CPD6+KWqc4z151MxSmfCenhGiabadn0\n03nfpFVeeQkK0rzPirGOVo7leMFOumuPcUK2bY562m+posvDL0rF4xJnzcX0CcPF\ngTeMUWVo9QKBgQDeJXxzoeBhygxf1UIWnij0pwx0BsynXsCONFJOILWfuCMouBgX\n+OxXPzrs8JpTQyHhw2qEYfJem8jmcQTiUX4mvvr1q7Uhac/J9q/xql/OpwnCEhnL\nM8x8DyFgIZk93kcuBeQbrNKmGcSDgoFI4BO/ev6iknENyXnKCvN5S6pz2wKBgCcE\nMQrjHYDfpNNRbhcaaVBg8QjlnMd1FqpaiTCjfSKyMre6fJMC4I8MmSJGLn7Qi1RB\n3rAMV4RGjSMQCNis3uOAbQwoqxL7MM9HN8tKO3cW3Y9LJ4tBJvOKMufUXNR/pxhb\nPuQ/pEwUn6GM6+6U8qowetW3CgAtgHiT9FYBKya9AoGASpnMzPXwGAtPJMWRvfB8\nJEKZryzuVe6N6vggeBmD6LqGVGI30cbynczwoXi8p4u1nN9+vAw7Up69mDX1Ysq6\n66LjKKfR90/G2h1esrd5LCHMXuc9u8rH8gzyYaWlujGI74lEqg/uE8/l+LWnRl3K\nZ3budWsV2n2j6OH0t6mnDu4=\n-----END PRIVATE KEY-----"
    
    credenciales_dict = {
        "type": "service_account",
        "project_id": "dulcesapp-485002",
        "private_key_id": "716d336781b7b019d9224341cc49492a183dd456",
        # ESTA ES LA LÍNEA MÁGICA QUE ARREGLA EL ERROR JWT:
        "private_key": clave_privada.replace("\\n", "\n"),
        "client_email": "robot-dulces@dulcesapp-485002.iam.gserviceaccount.com",
        "client_id": "111559915828770374333",
        "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token",
        "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
        "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/robot-dulces%40dulcesapp-485002.iam.gserviceaccount.com",
        "universe_domain": "googleapis.com"
    }

    creds = Credentials.from_service_account_info(credenciales_dict, scopes=scope)
    client = gspread.authorize(creds)
    return client

# --- LÓGICA DE LA APP ---
try:
    st.title("🍬 Gestión de Inventario - Proyecto Final")
    
    with st.spinner('Conectando a Google Sheets...'):
        # 1. Conectar
        client = obtener_conexion()
        
        # 2. Abrir la hoja por URL
        url_sheet = "https://docs.google.com/spreadsheets/d/1wVjGQBeoDL4biUwbjqRhkVW6H4zkbQu_0qDokP5s-uY/edit"
        sh = client.open_by_url(url_sheet)
        
        # 3. Seleccionar la primera pestaña
        worksheet = sh.sheet1
        
        # 4. Leer datos
        datos = worksheet.get_all_records()
        df = pd.DataFrame(datos)

    st.success("✅ ¡CONEXIÓN EXITOSA!")
    
    # MOSTRAR DATOS
    st.dataframe(df)

    # FORMULARIO DE PRUEBA
    st.divider()
    st.write("Prueba de escritura:")
    with st.form("nuevo_dulce"):
        nombre = st.text_input("Nombre")
        cantidad = st.number_input("Cantidad", min_value=1)
        btn = st.form_submit_button("Guardar")
        
        if btn and nombre:
            worksheet.append_row([nombre, cantidad])
            st.success("Guardado.")
            st.rerun()

except Exception as e:
    st.error(f"Error detallado: {e}")
