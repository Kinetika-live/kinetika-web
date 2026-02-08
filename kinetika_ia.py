import streamlit as st
import pandas as pd
import os
import time
import random
from datetime import datetime

# --- CONFIGURACIÓN DE LA PÁGINA ---
st.set_page_config(page_title="KINETIKA SYSTEM", page_icon="⚡", layout="wide")

# --- INTENTO DE CONEXIÓN CON ARDUINO (Seguro para Nube) ---
TRY_ARDUINO = False
try:
    import serial.tools.list_ports
    import serial
    # Solo activamos Arduino si NO estamos en un servidor de Streamlit
    # (Streamlit Cloud no tiene puertos USB, así que esto fallará allá y pasará al except)
    TRY_ARDUINO = True
except ImportError:
    TRY_ARDUINO = False

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
<style>
    .main-header { font-size: 30px; font-weight: bold; color: #2E86C1; text-align: center; }
    .sub-header { font-size: 18px; color: #555; text-align: center; margin-bottom: 20px;}
    .success-card {
        background-color: #d4edda; color: #155724; padding: 20px;
        border-radius: 10px; border: 1px solid #c3e6cb; text-align: center;
    }
    .lcd-container {
        background-color: #000; border: 4px solid #333; border-radius: 10px;
        padding: 15px; text-align: center; color: #0f0; font-family: 'Courier New', monospace;
    }
    .lcd-value { font-size: 50px; font-weight: bold; text-shadow: 0 0 10px #0f0; }
    .stButton>button { width: 100%; border-radius: 8px; height: 3em; font-weight: bold;}
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS (Simulada en CSV) ---
ARCHIVO_DB = "kinetika_db.csv"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DB):
        df = pd.DataFrame(columns=["Nombre", "Prioridad", "Puntaje", "Status", "Fecha"])
        df.to_csv(ARCHIVO_DB, index=False)
        return df
    return pd.read_csv(ARCHIVO_DB)

def guardar_registro(nombre, condicion):
    # LÓGICA DE PRIORIZACIÓN (EL CEREBRO DE LA IA)
    puntos = 100 # Base
    if "Soporte Vital" in condicion: puntos += 1000
    elif "Medicamento" in condicion: puntos += 500
    elif "Adulto Mayor" in condicion: puntos += 300
    elif "Calor" in condicion: puntos += 200
    
    # Factor Climático (Simulado para demostración)
    temp_actual = random.uniform(36.0, 41.0) 
    if temp_actual > 38.0:
        puntos += 50 # Bono por Ola de Calor
        
    df = cargar_datos()
    nuevo = pd.DataFrame({
        "Nombre": [nombre], 
        "Prioridad": [condicion], 
        "Puntaje": [puntos], 
        "Status": ["En Espera"],
        "Fecha": [datetime.now().strftime("%H:%M:%S")]
    })
    # Guardamos
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(ARCHIVO_DB, index=False)
    return puntos

# --- MENÚ DE NAVEGACIÓN ---
# Esto separa lo que ve el Juez (Celular) de lo que ves tú (Laptop)
menu = st.sidebar.radio("Selecciona Vista:", ["📱 Registro (Usuario)", "💻 Monitor (Stand)"])

# ==========================================
# VISTA 1: PARA EL JUEZ (REGISTRO)
# ==========================================
if menu == "📱 Registro (Usuario)":
    st.markdown("<div class='main-header'>⚡ KINETIKA</div>", unsafe_allow_html=True)
    st.markdown("<div class='sub-header'>Solicitud de Energía Inteligente</div>", unsafe_allow_html=True)
    
    with st.form("registro_form", clear_on_submit=True):
        st.info("Ingresa tus datos para que la IA evalúe tu prioridad.")
        nombre = st.text_input("Nombre del Solicitante")
        condicion = st.selectbox("Motivo de la Solicitud", [
            "🚑 Soporte Vital / Médico Crítico",
            "❄️ Medicamento Refrigerado",
            "👵 Adulto Mayor / Vulnerable",
            "🏠 Uso Doméstico General"
        ])
        enviar = st.form_submit_button("ENVIAR SOLICITUD")
        
    if enviar and nombre:
        pts = guardar_registro(nombre, condicion)
        st.balloons()
        mensaje = f"""
        <div class="success-card">
            <h3>✅ Solicitud Recibida</h3>
            <p><strong>Usuario:</strong> {nombre}</p>
            <p><strong>Nivel de Prioridad (IA):</strong> {pts} Puntos</p>
            <hr>
            <p style="font-size:12px">Tu caso ha sido enviado al Centro de Control Kinetika.</p>
        </div>
        """
        st.markdown(mensaje, unsafe_allow_html=True)

# ==========================================
# VISTA 2: PARA TU LAPTOP (MONITOR)
# ==========================================
elif menu == "💻 Monitor (Stand)":
    st.title("🎛️ Centro de Control KINETIKA")
    
    col1, col2 = st.columns([1, 1])
    
    # --- PANEL IZQUIERDO: LISTA DE IA ---
    with col1:
        st.subheader("📋 Triaje en Tiempo Real")
        if st.button("🔄 Actualizar Lista"):
            st.rerun()
            
        df = cargar_datos()
        if not df.empty:
            # Ordenamos para que el de más puntaje salga primero
            df = df.sort_values(by="Puntaje", ascending=False)
            
            # Mostramos al Ganador
            top_nombre = df.iloc[0]["Nombre"]
            top_puntos = df.iloc[0]["Puntaje"]
            top_motivo = df.iloc[0]["Prioridad"]
            
            st.info(f"🏆 PRIO #1: **{top_nombre}** ({top_puntos} pts)")
            st.caption(f"Motivo: {top_motivo}")
            
            st.dataframe(df[["Nombre", "Puntaje"]], hide_index=True, use_container_width=True)
        else:
            st.warning("Esperando solicitudes...")

    # --- PANEL DERECHO: GENERADOR ---
    with col2:
        st.subheader("⚡ Estado del Generador")
        st.caption("Modo: Simulación Cloud (Para Demo)")
        
        contenedor_lcd = st.empty()
        btn_start = st.button("▶️ ACTIVAR CARGA")
        
        if btn_start:
            # Barra de progreso
            bar = st.progress(0)
            
            # Simulación de carga (10 segundos)
            for i in range(100):
                # Voltaje aleatorio realista (11v a 14v)
                v = random.uniform(11.5, 14.2)
                
                # Color según voltaje
                color = "#ff3333" # Rojo (Bajo)
                estado = "BAJO"
                if v > 12.0: color = "orange"; estado="CARGANDO"
                if v > 13.5: color = "#33ff33"; estado="ÓPTIMO"
                
                # Renderizar LCD
                contenedor_lcd.markdown(f"""
                <div class="lcd-container">
                    <div style="color:{color}; font-size:20px;">{estado}</div>
                    <div class="lcd-value" style="color:{color}">{v:.1f} V</div>
                </div>
                """, unsafe_allow_html=True)
                
                time.sleep(0.05)
                bar.progress(i + 1)
            
            st.success("✅ CICLO COMPLETADO")
            st.balloons()