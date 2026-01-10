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

st.set_page_config(page_title="Ahorcado Pro Online", layout="centered")

# --- CSS ---
st.markdown("""
    <style>
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111; color: #00ff00; padding: 20px;
        border-radius: 10px; line-height: 1.2; font-size: 24px;
        white-space: pre; display: inline-block; border: 2px solid #444;
    }
    .word-box { 
        font-size: 45px; letter-spacing: 10px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 15px; font-family: monospace;
    }
    .v-bg { background-color: #28a745; padding: 60px 20px; border-radius: 20px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 60px 20px; border-radius: 20px; text-align: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo_texto(i):
    etapas = [
        "  +---+  \n  |   |  \n  O   |  \n /|\\  |  \n / \\  |  \n      |  \n=========",
        "  +---+  \n  |   |  \n  O   |  \n /|\\  |  \n /    |  \n      |  \n=========",
        "  +---+  \n  |   |  \n  O   |  \n /|\\  |  \n      |  \n      |  \n=========",
        "  +---+  \n  |   |  \n  O   |  \n /|   |  \n      |  \n      |  \n=========",
        "  +---+  \n  |   |  \n  O   |  \n  |   |  \n      |  \n      |  \n=========",
        "  +---+  \n  |   |  \n  O   |  \n      |  \n      |  \n      |  \n=========",
        "  +---+  \n  |   |  \n      |  \n      |  \n      |  \n      |  \n=========" 
    ]
    return etapas[i]

# --- LÓGICA DE REINICIO TOTAL ---
def reiniciar_todo():
    srv["palabra"] = ""
    srv["usadas"] = []
    srv["intentos"] = 6
    srv["gano_directo"] = False
    st.rerun()

# --- ESTADOS DEL JUEGO ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

# --- FLUJO DE PANTALLAS ---

# 1. Pantalla de Victoria
if ganado:
    st.markdown(f'<div class="v-bg"><h1>✨ ¡GANASTE!</h1><p>La palabra era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    if st.button("🔄 CREAR NUEVA PARTIDA", on_click=reiniciar_todo):
        pass

# 2. Pantalla de Derrota
elif perdido:
    st.markdown(f'<div class="d-bg"><h1>💀 PERDISTE</h1><p>La palabra era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<center><div class="dibujo-box">{obtener_dibujo_texto(0)}</div></center>', unsafe_allow_html=True)
    if st.button("🔄 REINTENTAR / NUEVA PALABRA", on_click=reiniciar_todo):
        pass

# 3. Pantalla Inicial (Escribir palabra)
elif not srv["palabra"]:
    st.title("🏹 Sala de Ahorcado Online")
    p_nueva = st.text_input("Escribe la palabra secreta para el grupo:", type="password")
    if st.button("🎮 EMPEZAR JUEGO"):
        if p_nueva:
            srv["palabra"] = p_nueva.lower().strip()
            srv["usadas"] = []
            srv["intentos"] = 6
            srv["gano_directo"] = False
            st.rerun()

# 4. Pantalla de Juego Activo
else:
    st.title("🗡️ Ahorcado en Tiempo Real")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f'<div class="dibujo-box">{obtener_dibujo_texto(srv["intentos"])}</div>', unsafe_allow_html=True)
    with c2:
        st.metric("Vidas", srv["intentos"])
        adivina = st.text_input("¿La sabes?", key="guess_input").lower().strip()
        if st.button("🎯 ADIVINAR"):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    cols = st.columns(7)
    for i, l in enumerate("abcdefghijklmnopqrstuvwxyz"):
        with cols[i % 7]:
            if l in srv["usadas"]:
                st.button("✅" if l in srv["palabra"] else "❌", key=f"btn-{l}", disabled=True)
            else:
                if st.button(l.upper(), key=f"btn-{l}"):
                    srv["usadas"].append(l)
                    if l not in srv["palabra"]: srv["intentos"] -= 1
                    st.rerun()
