import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {
        "palabra": "",
        "usadas": [],
        "intentos": 6,
        "gano_directo": False
    }

srv = obtener_servidor()

# Auto-refresco cada 2 segundos
st_autorefresh(interval=2000, key="datarefresh")

st.set_page_config(page_title="Ahorcado Clásico Online", layout="centered")

# --- CSS PARA EL DISEÑO ---
st.markdown("""
    <style>
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111;
        color: #00ff00;
        padding: 20px;
        border-radius: 10px;
        line-height: 1.2;
        font-size: 24px;
        white-space: pre;
        display: inline-block;
        border: 2px solid #444;
    }
    .word-box { 
        font-size: 45px; letter-spacing: 10px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 15px; font-family: monospace;
    }
    .v-bg { background-color: #28a745; padding: 80px 20px; border-radius: 20px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 80px 20px; border-radius: 20px; text-align: center; color: white; }
    .texto-final { font-size: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo_texto(i):
    # Dibujo clásico con caracteres estándar
    etapas = [
        "  +---+  \n  |   |  \n  O   |  \n /|\\  |  \n / \\  |  \n      |  \n=========", # 0: Muerto
        "  +---+  \n  |   |  \n  O   |  \n /|\\  |  \n /    |  \n      |  \n=========", # 1
        "  +---+  \n  |   |  \n  O   |  \n /|\\  |  \n      |  \n      |  \n=========", # 2
        "  +---+  \n  |   |  \n  O   |  \n /|   |  \n      |  \n      |  \n=========", # 3
        "  +---+  \n  |   |  \n  O   |  \n  |   |  \n      |  \n      |  \n=========", # 4
        "  +---+  \n  |   |  \n  O   |  \n      |  \n      |  \n      |  \n=========", # 5
        "  +---+  \n  |   |  \n      |  \n      |  \n      |  \n      |  \n========="  # 6: Vacío
    ]
    return etapas[i]

# --- LÓGICA ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.markdown(f'<div class="v-bg"><p class="texto-final">✨ ¡GANASTE!</p><p>La palabra era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    if st.button("NUEVA PARTIDA"): srv["palabra"] = ""; st.rerun()

elif perdido:
    st.markdown(f'<div class="d-bg"><p class="texto
