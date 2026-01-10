import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Ahorcado Online", layout="centered")

# --- CEREBRO COMPARTIDO (ESTO LO HACE ONLINE) ---
# Al usar @st.cache_resource, esta variable 's' es la misma para TODOS
@st.cache_resource
def obtener_juego():
    return {
        "palabra": "", 
        "usadas": [], 
        "intentos": 6, 
        "gano_directo": False,
        "tema": "oscuro"
    }

s = obtener_juego()

# --- SELECTOR DE TEMA ---
if st.button("🌓 Cambiar Color (Claro/Oscuro)"):
    s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
    st.rerun()

# --- CSS FUERTE (BORDES GRUESOS Y TECLADO FIJO) ---
fondo = "#0E1117" if s["tema"] == "oscuro" else "#FFFFFF"
texto = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"
btn_fondo = "#262730" if s["tema"] == "oscuro" else "#F0F2F6"
# Aquí definimos el color del borde (Gris oscuro o gris claro)
borde_color = "#444444" if s["tema"] == "oscuro" else "#999999"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {fondo}; color: {texto}; }}
    
    /* 1. OBLIGAR A QUE SE VEA EN FILA EN EL CELULAR (NO LISTA) */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    /* 2. BOTONES CON BORDE GRUESO Y TAMAÑO GRANDE */
    .stButton > button {{
        width: 100% !important;
        height: 60px !important;         /* Altura grande */
        font-size: 20px !important;      /* Letra grande */
        font-weight: bold !important;
        background-color: {btn_fondo} !important;
        color: {texto} !important;
        
        /* AQUÍ ESTÁ EL BORDE QUE PEDISTE */
        border: 3px solid {borde_color} !important; 
        border-radius: 10px !important;
        
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        padding: 0px !important;
    }}
    
    /* Estilos de texto */
    .palabra-box {{ font-size: 35px; font-weight: bold; color: #FFD700; text-align: center; letter-spacing: 8px; margin: 20px 0; font-family: monospace; }}
    .vidas-box {{ font-size: 24px; font-weight: bold; color: #FF4B4B; text-align: center; }}
    pre {{ background-color: #111 !important; color: #00FF00 !important; font-size: 18px !important; border: 2px solid #555; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

def dibujo(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\  | \n/ \  | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|\  | \n/    | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|\  | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======",
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n=======" 
    ]
    return etapas[i]

# --- LÓGICA DE JUEGO ---
if not s["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 CREAR PARTIDA"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado:
        st.balloons()
        st.success(f"🏆 ¡VICTORIA! ERA: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar)
    elif s["intentos"] <= 0:
        st.error(f"💀 DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # PANTALLA DE JUEGO
        st.markdown(f"<div class='vidas-box'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 1])
        with c1: st.code(dibujo(s["intentos"]))
        with c2:
            adv = st.text_input("🎯 ¿La sabes?", key="adv").lower().strip()
            if st.button("ENVIAR"):
                if adv == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()

        # Palabra
        txt = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-box'>{txt}</div>", unsafe_allow_html=True)

        # TECLADO FIJO (7 COLUMNAS)
        st.write("Teclado:")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        
        # Bucle exacto para filas de 7
        for i in range(0, len(abc), 7):
            fila = abc[i:i+7]
            cols = st.columns(7)
            for j, letra in enumerate(fila):
                l_min = letra.lower()
                with cols[j]:
                    if l_min in s["usadas"]:
                        # Muestra si acertó o falló
                        st.write("✅" if l_min in s["palabra"] else "❌")
                    else:
                        if st.button(letra, key=f"k-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()
        
        # ACTULIZACIÓN AUTOMÁTICA (ONLINE)
        time.sleep(2)
        st.rerun()
