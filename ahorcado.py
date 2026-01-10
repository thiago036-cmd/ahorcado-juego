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

st.set_page_config(page_title="Ahorcado Universal", layout="wide")

# --- CSS RESPONSIVO INTELIGENTE ---
st.markdown("""
    <style>
    /* Estilo base para el dibujo (ASCII) */
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
        margin: auto;
    }

    /* Ajustes para PC (Pantallas grandes) */
    @media (min-width: 800px) {
        .dibujo-box { font-size: 22px; width: 250px; }
        .word-box { font-size: 50px; letter-spacing: 15px; }
        .teclado-container { max-width: 600px; margin: auto; }
    }

    /* Ajustes para CELULAR (Pantallas pequeñas) */
    @media (max-width: 799px) {
        .dibujo-box { font-size: 5vw; width: 100%; }
        .word-box { font-size: 10vw; letter-spacing: 3vw; }
        .stButton > button { height: 55px !important; font-size: 20px !important; }
    }

    .word-box { 
        text-align: center; 
        margin: 20px 0; 
        color: #FFD700; 
        background: #262730; 
        border-radius: 15px; 
        padding: 15px; 
        font-family: monospace;
        font-weight: bold;
    }
    
    .v-bg { background-color: #28a745; padding: 50px; border-radius: 20px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 50px; border-radius: 20px; text-align: center; color: white; }
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

def reiniciar_todo():
    srv.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

# --- LÓGICA DE PANTALLAS ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.markdown(f'<div class="v-bg"><h1>👑 GANASTE</h1><p>Palabra: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
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
    # --- JUEGO ACTIVO ---
    # Usamos columnas que en móvil se apilan solas
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.markdown(f'<div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>', unsafe_allow_html=True)
    
    with col_der:
        st.metric("Vidas restantes", srv["intentos"])
        adivina = st.text_input("¿La tienes?", placeholder="Escribe la palabra...").lower().strip()
        if st.button("🎯 ADIVINAR TODO", use_container_width=True):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado que se adapta
    st.markdown('<div class="teclado-container">', unsafe_allow_html=True)
    abc = "abcdefghijklmnopqrstuvwxyz"
    # 7 columnas en PC, se ven bien. En móvil Streamlit las ajusta automáticamente
    cols = st.columns(7) 
    for i, l in enumerate(abc):
        with cols[i % 7]:
            if l in srv["usadas"]:
                st.button("✅" if l in srv["palabra"] else "❌", key=f"key-{l}", disabled=True)
            else:
                if st.button(l.upper(), key=f"key-{l}"):
                    srv["usadas"].append(l)
                    if l not in srv["palabra"]: srv["intentos"] -= 1
                    st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)

    # Refresco automático
    time.sleep(3)
    st.rerun()
