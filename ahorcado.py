import streamlit as st
import time

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

srv = obtener_servidor()

st.set_page_config(page_title="Ahorcado Pro", layout="centered")

# --- CSS PARA ORDEN VERTICAL Y CORAZÓN ---
st.markdown("""
    <style>
    /* Contenedor principal alineado verticalmente */
    .main-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        width: 100%;
    }

    /* Dibujo ASCII */
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111;
        color: #00ff00;
        padding: 20px;
        border-radius: 10px;
        line-height: 1.2;
        white-space: pre;
        border: 2px solid #444;
        text-align: center;
        font-size: 22px;
        margin-bottom: 10px;
    }

    /* Contador de Vidas al lado del dibujo */
    .vidas-text {
        color: #ff4b4b;
        font-size: 24px;
        font-weight: bold;
        margin-bottom: 20px;
        text-align: center;
    }

    /* Palabra oculta */
    .word-box { 
        font-size: 40px; 
        letter-spacing: 10px; 
        text-align: center; 
        margin: 20px 0; 
        color: #FFD700; 
        background: #262730; 
        border-radius: 15px; 
        padding: 20px; 
        font-family: monospace;
        width: 100%;
    }

    /* Botones de letras */
    .stButton > button {
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
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
    st.success("✨ ¡GANASTE!")
    st.button("🔄 NUEVA PARTIDA", on_click=reiniciar_todo)
elif perdido:
    st.error(f"💀 PERDISTE. Era: {srv['palabra'].upper()}")
    st.button("🔄 REINTENTAR", on_click=reiniciar_todo)
elif not srv["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("EMPEZAR"):
        if p:
            srv.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    # --- JUEGO ACTIVO (ORDEN VERTICAL) ---
    
    # 1. Dibujo
    st.markdown(f'<center><div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div></center>', unsafe_allow_html=True)
    
    # 2. Vidas con Corazón (donde apuntaba la flecha)
    st.markdown(f'<div class="vidas-text">Vidas: ❤️ {srv["intentos"]}</div>', unsafe_allow_html=True)
    
    # 3. Input para adivinar palabra completa
    adivina = st.text_input("¿Ya sabes la palabra?", key="full_guess").lower().strip()
    if st.button("ADIVINAR PALABRA"):
        if adivina == srv["palabra"]: srv["gano_directo"] = True
        else: srv["intentos"] = 0
        st.rerun()

    # 4. Espacio de la palabra
    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # 5. Teclado
    st.write("### Selecciona una letra:")
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    for fila in [abc[i:i+7] for i in range(0, len(abc), 7)]:
        cols = st.columns(7)
        for i, letra in enumerate(fila):
            l_min = letra.lower()
            with cols[i]:
                if l_min in srv["usadas"]:
                    st.button("✅" if l_min in srv["palabra"] else "❌", key=f"k-{l_min}", disabled=True)
                else:
                    if st.button(letra, key=f"k-{l_min}"):
                        srv["usadas"].append(l_min)
                        if l_min not in srv["palabra"]: srv["intentos"] -= 1
                        st.rerun()

    time.sleep(3)
    st.rerun()
