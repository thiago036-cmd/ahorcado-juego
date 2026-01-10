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

# Configuración para que se adapte a móviles
st.set_page_config(page_title="Ahorcado Mobile", layout="centered", initial_sidebar_state="collapsed")

# --- LÓGICA DE REINICIO ---
def reiniciar_todo():
    srv.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

# --- CSS OPTIMIZADO PARA CELULAR ---
st.markdown("""
    <style>
    /* Ajuste del dibujo para que no se desborde en pantallas pequeñas */
    .dibujo-box { 
        font-family: monospace; 
        background-color: #111; 
        color: #00ff00; 
        padding: 10px; 
        border-radius: 10px; 
        line-height: 1.1; 
        font-size: 5vw; /* Tamaño basado en el ancho de la pantalla */
        white-space: pre; 
        display: block; 
        border: 2px solid #444;
        text-align: center;
    }
    /* Palabra con letras que se ajustan */
    .word-box { 
        font-size: 8vw; 
        letter-spacing: 2vw; 
        text-align: center; 
        margin: 10px 0; 
        color: #FFD700; 
        background: #262730; 
        border-radius: 10px; 
        padding: 10px; 
        font-family: monospace;
        word-wrap: break-word;
    }
    /* Botones del teclado más altos para dedos */
    .stButton > button {
        width: 100%;
        height: 50px !important;
        padding: 0px !important;
        font-size: 18px !important;
    }
    .v-bg { background-color: #28a745; padding: 40px 10px; border-radius: 15px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 40px 10px; border-radius: 15px; text-align: center; color: white; }
    
    /* Quitar espacios inútiles en móvil */
    .main .block-container { padding-top: 1rem; padding-bottom: 1rem; }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | \n=======", # 0
        " +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | \n=======", # 1
        " +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | \n=======", # 2
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======", # 3
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======", # 4
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======", # 5
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n======="  # 6
    ]
    return etapas[i]

# --- FLUJO DEL JUEGO ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.markdown(f'<div class="v-bg"><h1>✨ ¡VICTORIA!</h1><p>Era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.button("🔄 NUEVA PARTIDA", on_click=reiniciar_todo, use_container_width=True)
elif perdido:
    st.markdown(f'<div class="d-bg"><h1>💀 PERDISTE</h1><p>Era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<div class="dibujo-box">{obtener_dibujo(0)}</div>', unsafe_allow_html=True)
    st.button("🔄 REINTENTAR", on_click=reiniciar_todo, use_container_width=True)
elif not srv["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("EMPEZAR JUEGO", use_container_width=True):
        if p:
            srv.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    # JUEGO ACTIVO
    st.markdown(f'<div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>', unsafe_allow_html=True)
    
    col_v, col_a = st.columns([1, 2])
    col_v.metric("Vidas", srv["intentos"])
    with col_a:
        adivina = st.text_input("¿La sabes?", key="guess_mob", label_visibility="collapsed", placeholder="Palabra completa...")
        if st.button("🎯 ADIVINAR", use_container_width=True):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado optimizado (4 columnas en móvil)
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(4) 
    for i, l in enumerate(abc):
        with cols[i % 4]:
            if l in srv["usadas"]:
                st.button("✅" if l in srv["palabra"] else "❌", key=f"m-{l}", disabled=True)
            else:
                if st.button(l.upper(), key=f"m-{l}"):
                    srv["usadas"].append(l)
                    if l not in srv["palabra"]: srv["intentos"] -= 1
                    st.rerun()

    # Refresco automático cada 3 segundos
    time.sleep(3)
    st.rerun()
