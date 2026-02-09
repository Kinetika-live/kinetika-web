import streamlit as st
import pandas as pd
import os
import random
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="KINETIKA: Alta de Solicitudes", page_icon="📝", layout="wide")

# --- ESTILOS VISUALES (LIMPIOS Y SERIOS) ---
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
ARCHIVO_DB = "kinetika_db_final.csv"

def cargar_datos():
    if not os.path.exists(ARCHIVO_DB):
        cols = ["Nombre", "Telefono", "Direccion", "Zona", "Edad", "Personas", "Condicion", "Puntaje", "Status", "Fecha"]
        df = pd.DataFrame(columns=cols)
        df.to_csv(ARCHIVO_DB, index=False)
        return df
    return pd.read_csv(ARCHIVO_DB)

def guardar_registro(nombre, tel, dir_in, zona, edad, pers, cond):
    # --- ALGORITMO INTERNO (INVISIBLE AL USUARIO) ---
    puntos = 100 
    
    # 1. CRITERIO DE SUPERVIVENCIA
    if "Soporte Vital" in cond: puntos += 1000
    elif "Medicamento" in cond: puntos += 500
    elif "Adulto Mayor" in cond: puntos += 300
    elif "Emergencia Civil" in cond: puntos += 800
    elif "Escuela" in cond: puntos += 300
    
    # 2. CRITERIO DE RED DE APOYO (JUSTICIA SOCIAL)
    if pers <= 2:
        puntos += 200  # Prioridad Alta (Cuidador solo)
    elif pers <= 4:
        puntos += 100  # Prioridad Media
    else:
        puntos += 20   # Prioridad Baja
    
    # 3. FACTOR CLIMÁTICO (Simulado)
    temp_actual = random.uniform(36.0, 41.0) 
    if temp_actual > 38.0 and (edad > 60 or edad < 5):
        puntos += 150 
        
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
