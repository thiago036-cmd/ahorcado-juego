import streamlit as st
import time

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

srv = obtener_servidor()

st.set_page_config(page_title="Ahorcado Pro", layout="centered")

# --- CSS PARA ALINEACIÓN VERTICAL Y TECLADO FIJO ---
st.markdown("""
    <style>
    /* Forzar que las columnas NO se apilen en vertical en el celular */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
    }
    
    /* Ajuste de los botones del teclado */
    div[data-testid="stHorizontalBlock"] > div {
        width: 14% !important; /* Esto asegura 7 letras por fila siempre */
        min-width: 40px !important;
        flex: none !important;
    }

    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111; color: #00ff00; padding: 15px;
        border-radius: 10px; line-height: 1.1; white-space: pre;
        border: 2px solid #444; font-size: 20px;
        display: inline-block;
    }

    .vidas-container {
        display: inline-block;
        vertical-align: top;
        margin-left: 15px;
        padding-top: 20px;
        color: white;
        font-size: 24px;
        font-weight: bold;
    }

    .word-box { 
        font-size: 35px; letter-spacing: 10px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 15px; font-family: monospace;
        width: 100%;
    }

    /* Estilo para los botones */
    .stButton > button {
        width: 100% !important;
        padding: 5px 0px !important;
        font-size: 16px !important;
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

# --- LÓGICA ---
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
    # --- JUEGO ACTIVO ---
    
    # Dibujo y Vidas al lado (como pediste en el dibujo rojo)
    st.markdown(f"""
        <div style="text-align: center;">
            <div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>
            <div class="vidas-container">Vidas:<br>❤️ {srv["intentos"]}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # Alineación vertical de lo que estaba en verde
    st.write("") # Espaciador
    adivina = st.text_input("¿La sabes?", key="full_input", placeholder="Adivinar palabra entera...").lower().strip()
    if st.button("ADIVINAR", use_container_width=True):
        if adivina == srv["palabra"]: srv["gano_directo"] = True
        else: srv["intentos"] = 0
        st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado en cuadrícula de 7 columnas fija
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
