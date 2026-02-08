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
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; font-weight: bold; background-color: #2E86C1; color: white;}
    .priority-card {
        background-color: #f8f9fa; border-left: 5px solid #2E86C1; padding: 20px; border-radius: 5px; margin-bottom: 20px;
    }
    .data-label { font-weight: bold; color: #555; }
</style>
""", unsafe_allow_html=True)

# --- BASE DE DATOS ---
ARCHIVO_DB = "kinetika_db_v2.csv"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DB):
        cols = ["Nombre", "Telefono", "Direccion", "Zona", "Edad", "Personas", "Condicion", "Puntaje", "Status", "Fecha"]
        df = pd.DataFrame(columns=cols)
        df.to_csv(ARCHIVO_DB, index=False)
        return df
    return pd.read_csv(ARCHIVO_DB)

def guardar_registro(nombre, tel, dir_in, zona, edad, pers, cond):
    # LÓGICA DE PRIORIZACIÓN (ALGORITMO ÉTICO)
    puntos = 100 
    if "Soporte Vital" in cond: puntos += 1000
    elif "Medicamento" in cond: puntos += 500
    elif "Adulto Mayor" in cond: puntos += 300
    elif "Emergencia Civil" in cond: puntos += 800
    elif "Escuela" in cond: puntos += 300
    
    # Factor Climático Simulado (Invisible al usuario)
    temp_actual = random.uniform(36.0, 41.0) 
    if temp_actual > 38.0 and (edad > 60 or edad < 5):
        puntos += 150 # Bono por vulnerabilidad al calor
        
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

# --- MENÚ OCULTO (Para que el usuario no se pierda) ---
vista = st.sidebar.radio("Navegación", ["📝 Alta Solicitud", "💻 Monitor (Stand)"])

# ==========================================
# VISTA 1: ALTA DE SOLICITUDES (USUARIO)
# ==========================================
if vista == "📝 Alta Solicitud":
    st.markdown("<div class='main-header'>📄 Alta de Solicitudes</div>", unsafe_allow_html=True)
    
    with st.form("form_registro", clear_on_submit=True):
        st.write("Por favor ingresa los datos requeridos.")
        
        # DISEÑO CORREGIDO (1 y 2 IZQ | 3 y 4 DER)
        col_izq, col_der = st.columns(2)
        
        # --- COLUMNA IZQUIERDA (Secciones 1 y 2) ---
        with col_izq:
            # SECCIÓN 1
            st.markdown("<div class='section-header'>1. Identificación</div>", unsafe_allow_html=True)
            nom = st.text_input("Nombre Responsable")
            tel = st.text_input("Teléfono / WhatsApp")
            
            # SECCIÓN 2
            st.markdown("<div class='section-header'>2. Perfil</div>", unsafe_allow_html=True)
            edad = st.number_input("Edad Beneficiario", 0, 110, step=1)
            pers = st.number_input("Personas en hogar", 1, 30, 4)

        # --- COLUMNA DERECHA (Secciones 3 y 4) ---
        with col_der:
            # SECCIÓN 3
            st.markdown("<div class='section-header'>3. Necesidad</div>", unsafe_allow_html=True)
            cond = st.selectbox("Condición Crítica:", [
                "🚑 Soporte Vital / Médico Crítico",
                "❄️ Salud: Medicamento Refrigerado",
                "👵 Adulto Mayor / Discapacidad",
                "🌪️ Emergencia Civil",
                "📚 Escuela / Educación",
                "🏠 Hogar General"
            ])
            
            # SECCIÓN 4
            st.markdown("<div class='section-header'>4. Ubicación</div>", unsafe_allow_html=True)
            dir_in = st.text_input("Dirección (Calle y Número)")
            zonas = ["San Miguel (La Bajada)", "San Miguel (Centro)", "Los Mochis (Centro)", 
                     "Los Mochis (Norte)", "Los Mochis (Sur)", "Zona Rural", "Otro"]
            zona = st.selectbox("Zona", zonas)

        st.markdown("---")
        # Botón Guardar
        enviar = st.form_submit_button("GUARDAR REGISTRO")
        
    if enviar:
        if nom and tel and dir_in:
            guardar_registro(nom, tel, dir_in, zona, edad, pers, cond)
            st.success("✅ Registro guardado exitosamente en el sistema Kinetika.")
        else:
            st.error("⚠️ Faltan datos obligatorios (Nombre, Teléfono o Dirección).")

# ==========================================
# VISTA 2: MONITOR
# ==========================================
elif vista == "💻 Monitor (Stand)":
    st.title("📋 Triaje en Tiempo Real")
    
    col_lista, col_detalle = st.columns([1, 1])
    
    df = cargar_datos()
    
    # --- LADO IZQUIERDO: LA LISTA ---
    with col_lista:
        if st.button("🔄 ACTUALIZAR LISTA"):
            st.rerun()
            
        if not df.empty:
            df = df.sort_values(by="Puntaje", ascending=False)
            st.dataframe(df[["Nombre", "Puntaje", "Condicion"]], hide_index=True, use_container_width=True)
        else:
            st.info("No hay solicitudes pendientes.")

    # --- LADO DERECHO: DETALLE COMPLETO (FICHA TÉCNICA) ---
    with col_detalle:
        st.subheader("🏆 PRIO #1: DETALLE DE ENTREGA")
        
        if not df.empty:
            top = df.iloc[0] # El primero de la lista
            
            # TARJETA DE INFORMACIÓN COMPLETA
            st.markdown(f"""
            <div class="priority-card">
                <h3>👤 {top['Nombre']}</h3>
                <p><span class="data-label">🚨 Motivo:</span> {top['Condicion']}</p>
                <p><span class="data-label">📍 Dirección:</span> {top['Direccion']}</p>
                <p><span class="data-label">🌍 Zona:</span> {top['Zona']}</p>
                <p><span class="data-label">📞 Contacto:</span> {top['Telefono']}</p>
                <hr>
                <p><span class="data-label">🎂 Edad:</span> {top['Edad']} años | <span class="data-label">🏠 Gente:</span> {top['Personas']}</p>
                <p><span class="data-label">💯 SCORE IA:</span> {top['Puntaje']} Pts</p>
            </div>
            """, unsafe_allow_html=True)
            
            st.warning("⚠️ Verificar disponibilidad de batería antes de despachar.")
        else:
            st.write("Esperando datos para análisis...")
