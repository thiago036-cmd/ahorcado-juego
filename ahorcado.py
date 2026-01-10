import streamlit as st
import time

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

st.set_page_config(page_title="Ahorcado Pro", layout="centered")

# --- CSS RESPONSIVO MEJORADO ---
st.markdown("""
    <style>
    /* Contenedor del Dibujo */
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111;
        color: #00ff00;
        padding: 15px;
        border-radius: 10px;
        line-height: 1.1;
        white-space: pre;
        border: 2px solid #444;
        text-align: center;
        margin: 10px auto;
        width: fit-content;
    }

    /* Palabra Oculta */
    .word-box { 
        font-size: 10vw; 
        letter-spacing: 2vw; 
        text-align: center; 
        margin: 20px 0; 
        color: #FFD700; 
        background: #262730; 
        border-radius: 15px; 
        padding: 15px; 
        font-family: monospace;
    }

    /* Pantallas de Fin */
    .v-bg { background-color: #28a745; padding: 40px; border-radius: 20px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 40px; border-radius: 20px; text-align: center; color: white; }

    /* Forzar que los botones no se amontonen en móvil */
    div[data-testid="stHorizontalBlock"] {
        flex-wrap: wrap !important;
        gap: 5px !important;
    }
    
    .stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
    }

    @media (min-width: 800px) {
        .word-box { font-size: 50px; letter-spacing: 15px; }
        .dibujo-box { font-size: 24px; }
    }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======", 
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n======="  
    ]
    return etapas[i]

def reiniciar_todo():
    srv.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

# --- LÓGICA DE ESTADOS ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.markdown(f'<div class="v-bg"><h1>✨ ¡GANASTE!</h1><p>Palabra: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.button("🔄 JUGAR OTRA VEZ", on_click=reiniciar_todo, use_container_width=True)

elif perdido:
    st.markdown(f'<div class="d-bg"><h1>💀 PERDISTE</h1><p>Era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dibujo-box">{obtener_dibujo(0)}</div>', unsafe_allow_html=True)
    st.button("🔄 REINTENTAR", on_click=reiniciar_todo, use_container_width=True)

elif not srv["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR", use_container_width=True):
        if p:
            srv.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()

else:
    # --- JUEGO ACTIVO ---
    st.markdown(f'<div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>', unsafe_allow_html=True)
    
    c_m, c_i = st.columns([1, 1])
    c_m.metric("Vidas", srv["intentos"])
    with c_i:
        adivina = st.text_input("¿La sabes?", key="full", placeholder="Escribe...").lower().strip()
        if st.button("🎯 ADIVINAR", use_container_width=True):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado con ajuste automático de columnas
    abc = "abcdefghijklmnopqrstuvwxyz"
    # Usamos un número menor de columnas para que en móvil no colapsen
    num_cols = 4 if st.session_state.get('viewport_width', 1000) < 600 else 7
    cols = st.columns(4 if ganado or perdido or True else 7) # Forzamos 4 para que sea seguro en móvil
    
    for i, l in enumerate(abc):
        with cols[i % 4]: # En celular 4 es el número mágico
            if l in srv["usadas"]:
                st.button("✅" if l in srv["palabra"] else "❌", key=f"k-{l}", disabled=True)
            else:
                if st.button(l.upper(), key=f"k-{l}"):
                    srv["usadas"].append(l)
                    if l not in srv["palabra"]: srv["intentos"] -= 1
                    st.rerun()

    time.sleep(3)
    st.rerun()
