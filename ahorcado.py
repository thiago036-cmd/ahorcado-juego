import streamlit as st
import time

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

srv = obtener_servidor()

st.set_page_config(page_title="Ahorcado Pro", layout="centered")

# --- CSS PARA QUE SE VEA IGUAL EN TODO DISPOSITIVO ---
st.markdown("""
    <style>
    /* Forzar que las columnas no se rompan en el celular */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 2px !important;
    }
    
    /* Tamaño fijo para las letras del teclado */
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Caja del dibujo ASCII */
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111; color: #00ff00; padding: 10px;
        border-radius: 10px; line-height: 1.1; white-space: pre;
        border: 2px solid #444; font-size: 18px;
        display: inline-block;
    }

    /* Vidas con Corazón */
    .vidas-container {
        display: inline-block;
        vertical-align: top;
        margin-left: 10px;
        color: white;
        font-size: 20px;
        font-weight: bold;
        text-align: left;
    }

    /* Caja de la palabra (Amarilla) */
    .word-box { 
        font-size: 30px; letter-spacing: 5px; text-align: center; 
        margin: 15px 0; color: #FFD700; background: #262730; 
        border-radius: 12px; padding: 15px; font-family: monospace;
    }

    /* Estilo botones teclado */
    .stButton > button {
        width: 100% !important;
        height: 40px !important;
        padding: 0px !important;
        font-size: 14px !important;
        border-radius: 5px !important;
    }
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

# --- LÓGICA ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.success("✨ ¡GANASTE!")
    st.button("🔄 NUEVA PARTIDA", on_click=reiniciar_todo)
elif perdido:
    st.error(f"💀 PERDISTE. La palabra era: {srv['palabra'].upper()}")
    st.button("🔄 REINTENTAR", on_click=reiniciar_todo)
elif not srv["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("EMPEZAR"):
        if p:
            srv.update({"palabra": p.lower().strip().replace('ñ', 'ñ'), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    # --- UI JUEGO ---
    
    # 1. Dibujo y Vidas al lado (❤️)
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 10px;">
            <div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>
            <div class="vidas-container">Vidas:<br>❤️ {srv["intentos"]}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Adivinar palabra completa
    adivina = st.text_input("¿La sabes?", key="full_input", placeholder="Escribir...").lower().strip()
    if st.button("🎯 ADIVINAR TODO", use_container_width=True):
        if adivina == srv["palabra"]: srv["gano_directo"] = True
        else: srv["intentos"] = 0
        st.rerun()

    # 3. Visualización de la palabra (Guiones)
    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # 4. Teclado con Ñ y 7 columnas fijas
    abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    # Dividimos el abecedario en grupos de 7 para mantener la cuadrícula
    for i in range(0, len(abc), 7):
        fila = abc[i:i+7]
        cols = st.columns(7)
        for j, letra in enumerate(fila):
            l_min = letra.lower()
            with cols[j]:
                if l_min in srv["usadas"]:
                    st.button("✅" if l_min in srv["palabra"] else "❌", key=f"k-{l_min}", disabled=True)
                else:
                    if st.button(letra, key=f"k-{l_min}"):
                        srv["usadas"].append(l_min)
                        if l_min not in srv["palabra"]: srv["intentos"] -= 1
                        st.rerun()

    time.sleep(3)
    st.rerun()
