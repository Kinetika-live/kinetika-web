import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA PROFESIONAL ---
st.set_page_config(page_title="KINETIKA: Alta de Solicitudes", page_icon="📝", layout="wide")

# --- ESTILOS VISUALES ---
st.markdown("""
<style>
    .main-header { font-size: 24px; font-weight: bold; color: #333; margin-bottom: 20px; }
    .section-header { font-size: 18px; font-weight: bold; color: #2E86C1; margin-top: 10px; border-bottom: 2px solid #eee; padding-bottom: 5px; }
    
    /* AQUÍ ESTÁ EL TRUCO: !important OBLIGA AL BOTÓN A SER VERDE */
    div.stButton > button { 
        width: 100%; 
        border-radius: 5px; 
        height: 3em; 
        font-weight: bold; 
        background-color: #28a745 !important; /* Color Verde Forzado */
        color: white !important;
        border: none !important;
    }
    div.stButton > button:hover {
        background-color: #218838 !important; /* Verde más oscuro al pasar el mouse */
        color: white !important;
    }

    .priority-card {
        background-color: #f8f9fa; border-left: 5px solid #2E86C1; padding: 20px; border-radius: 5px; margin-bottom: 20px;
    }
    .data-label { font-weight: bold; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ---
ARCHIVO_DB = "kinetika_db_final.csv"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DB):
        cols = ["Nombre", "Telefono", "Direccion", "Zona", "Edad", "Personas", "Condicion", "Puntaje", "Status", "Fecha"]
        df = pd.DataFrame(columns=cols)
        df.to_csv(ARCHIVO_DB, index=False)
        return df
    return pd.read_csv(ARCHIVO_DB)

def guardar_registro(nombre, tel, dir_in, zona, edad, pers, cond):
    # --- EL ALGORITMO ÉTICO (DISEÑADO POR EL EQUIPO) ---
    puntos = 100 
    
    # 1. CRITERIO DE SUPERVIVENCIA (Médico)
    if "Soporte Vital" in cond: puntos += 1000
    elif "Medicamento" in cond: puntos += 500
    elif "Adulto Mayor" in cond: puntos += 300
    elif "Emergencia Civil" in cond: puntos += 800
    elif "Escuela" in cond: puntos += 300
    
    # 2. CRITERIO DE RED DE APOYO (JUSTICIA SOCIAL)
    # Menos personas = Más vulnerabilidad del cuidador = MÁS PUNTOS
    if pers <= 2:
        puntos += 200  # 🚨 PRIORIDAD ALTA: Riesgo de colapso del cuidador
    elif pers <= 4:
        puntos += 100  # ⚠️ PRIORIDAD MEDIA: Familia pequeña
    else:
        puntos += 20   # ✅ ESTABLE: Red de apoyo suficiente
    
    # 3. FACTOR CLIMÁTICO (Simulado)
    # Simula si hay ola de calor en ese momento
    temp_actual = random.uniform(36.0, 41.0) 
    if temp_actual > 38.0 and (edad > 60 or edad < 5):
        puntos += 150 # Bono por Golpe de Calor
        
    df = cargar_datos()
    nuevo = pd.DataFrame({
        "Nombre": [nombre], "Telefono": [tel], "Direccion": [dir_in], "Zona": [zona],
        "Edad": [edad], "Personas": [pers], "Condicion": [cond],
        "Puntaje": [puntos], "Status": ["Pendiente"],
        "Fecha": [datetime.now().strftime("%Y-%m-%d %H:%M")]
    })
    df = pd.concat([df, nuevo], ignore_index=True)
    df.to_csv(ARCHIVO_DB, index=False)
    return True

# --- MENÚ DE NAVEGACIÓN ---
vista = st.sidebar.radio("Navegación", ["📝 Alta Solicitud", "💻 Monitor (Stand)"])

# ==========================================
# VISTA 1: ALTA DE SOLICITUDES (USUARIO)
# ==========================================
if vista == "📝 Alta Solicitud":
    st.markdown("<div class='main-header'>📄 Alta de Solicitudes</div>", unsafe_allow_html=True)
    
    with st.form("form_registro", clear_on_submit=True):
        st.write("COMPLETE LOS CAMPOS PARA SU EVALUACIÓN.")
        
        # DISEÑO ERGONÓMICO: (Identidad/Perfil) vs (Necesidad/Ubicación)
        col_izq, col_der = st.columns(2)
        
        # --- COLUMNA IZQUIERDA ---
        with col_izq:
            st.markdown("<div class='section-header'>1. Identificación</div>", unsafe_allow_html=True)
            nom = st.text_input("Nombre Responsable")
            tel = st.text_input("Teléfono / WhatsApp")
            
            st.markdown("<div class='section-header'>2. Perfil del Hogar</div>", unsafe_allow_html=True)
            edad = st.number_input("Edad del Beneficiario", 0, 110, step=1)
            pers = st.number_input("Personas en la vivienda", 1, 30, 2, help="Menos personas aumentan la prioridad por falta de relevos.")

        # --- COLUMNA DERECHA ---
        with col_der:
            st.markdown("<div class='section-header'>3. Necesidad Crítica</div>", unsafe_allow_html=True)
            cond = st.selectbox("Condición:", [
                "🚑 Soporte Vital / Médico Crítico",
                "❄️ Salud: Medicamento Refrigerado",
                "👵 Adulto Mayor / Discapacidad",
                "🌪️ Emergencia Civil",
                "📚 Escuela / Educación",
                "🏠 Hogar General"
            ])
            
            st.markdown("<div class='section-header'>4. Ubicación</div>", unsafe_allow_html=True)
            dir_in = st.text_input("Dirección (Calle y Número)")
            zonas = ["San Miguel (La Bajada)", "San Miguel (Centro)", "Los Mochis (Centro)", 
                     "Los Mochis (Norte)", "Los Mochis (Sur)", "Zona Rural", "Otro"]
            zona = st.selectbox("Zona", zonas)

        st.markdown("---")
        enviar = st.form_submit_button("ENVIAR REGISTRO")
        
    if enviar:
        if nom and tel and dir_in:
            guardar_registro(nom, tel, dir_in, zona, edad, pers, cond)
            st.success("✅ Solicitud procesada.")
        else:
            st.error("⚠️ Error: Datos incompletos.")

# ==========================================
# VISTA 2: MONITOR (LOGÍSTICA)
# ==========================================
elif vista == "💻 Monitor (Stand)":
    st.title("📋 Triaje de Beneficiarios")
    
    col_lista, col_detalle = st.columns([1, 1])
    
    df = cargar_datos()
    
    # --- LISTA DE ESPERA ---
    with col_lista:
        if st.button("🔄 ACTUALIZAR LISTA"):
            st.rerun()
            
        if not df.empty:
            df = df.sort_values(by="Puntaje", ascending=False)
            st.dataframe(df[["Nombre", "Puntaje", "Condicion"]], hide_index=True, use_container_width=True)
        else:
            st.info("Sistema en espera de solicitudes...")

    # --- FICHA DE ENTREGA ---
    with col_detalle:
        st.subheader("🏆 ASIGNACIÓN INMEDIATA")
        
        if not df.empty:
            top = df.iloc[0] # El Ganador
            
            st.markdown(f"""
            <div class="priority-card">
                <h3>👤 {top['Nombre']}</h3>
                <p><span class="data-label">🚨 Condición:</span> {top['Condicion']}</p>
                <p><span class="data-label">📍 Ubicación:</span> {top['Direccion']} ({top['Zona']})</p>
                <hr>
                <p><span class="data-label">🏠 Red de Apoyo:</span> {top['Personas']} personas</p>
                <p><span class="data-label">🎂 Edad Paciente:</span> {top['Edad']} años</p>
                <div style="background-color: #e2e6ea; padding: 10px; border-radius: 5px; margin-top: 10px; text-align: center;">
                    <span class="data-label">SCORE DE URGENCIA:</span><br>
                    <span style="font-size: 30px; color: #2E86C1; font-weight: bold;">{top['Puntaje']} Pts</span>
                </div>
            </div>
            """, unsafe_allow_html=True)
            
            st.success("✅ Batería Kinetika Autorizada para entrega.")
        else:
            st.write("Sin datos para analizar.")





