import streamlit as st
import time

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

srv = obtener_servidor()

st.set_page_config(page_title="Ahorcado Pro", layout="centered")

# --- CSS PARA DISEÑO FIJO, Ñ Y BOTONES GRANDES ---
st.markdown("""
    <style>
    /* Forzar cuadrícula de 7 columnas en cualquier pantalla */
    [data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        justify-content: center !important;
        gap: 5px !important;
    }
    
    /* Ajuste de cada contenedor de botón */
    div[data-testid="stHorizontalBlock"] > div {
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }

    /* Dibujo ASCII */
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111; color: #00ff00; padding: 15px;
        border-radius: 10px; line-height: 1.1; white-space: pre;
        border: 2px solid #444; font-size: 22px;
        display: inline-block;
    }

    /* Vidas con Corazón a la derecha */
    .vidas-container {
        display: inline-block;
        vertical-align: top;
        margin-left: 20px;
        color: white;
        font-size: 26px;
        font-weight: bold;
        text-align: left;
    }

    /* Palabra Amarilla (Sección Verde en tu dibujo) */
    .word-box { 
        font-size: 40px; letter-spacing: 10px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 25px; font-family: monospace;
        width: 100%;
        border: 1px solid #444;
    }

    /* BOTONES MÁS GRANDES (Lo que pediste) */
    .stButton > button {
        width: 100% !important;
        height: 60px !important; /* Más alto */
        font-size: 20px !important; /* Letra más grande */
        font-weight: bold !important;
        border-radius: 8px !important;
        background-color: #31333F !important;
        border: 1px solid #444 !important;
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

# --- LÓGICA DE JUEGO ---
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
    # --- PANTALLA DE JUEGO ---
    
    # 1. Dibujo y Vidas (❤️)
    st.markdown(f"""
        <div style="text-align: center; margin-bottom: 20px;">
            <div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>
            <div class="vidas-container">Vidas:<br>❤️ {srv["intentos"]}</div>
        </div>
    """, unsafe_allow_html=True)
    
    # 2. Input Adivinar
    adivina = st.text_input("¿La sabes?", key="full_guess_f", placeholder="Escribe la palabra...").lower().strip()
    if st.button("ADIVINAR", use_container_width=True):
        if adivina == srv["palabra"]: srv["gano_directo"] = True
        else: srv["intentos"] = 0
        st.rerun()

    # 3. Palabra Secreta (Sección Verde)
    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # 4. Teclado SIN duplicados y con Ñ
    st.write("### Selecciona una letra:")
    abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    
    # Dividimos exactamente en filas de 7 para que no se repitan
    filas = [abc[i:i+7] for i in range(0, len(abc), 7)]
    
    for fila in filas:
        cols = st.columns(7)
        for i, letra in enumerate(fila):
            l_min = letra.lower()
            with cols[i]:
                if l_min in srv["usadas"]:
                    st.button("✅" if l_min in srv["palabra"] else "❌", key=f"btn-{l_min}", disabled=True)
                else:
                    if st.button(letra, key=f"btn-{l_min}"):
                        srv["usadas"].append(l_min)
                        if l_min not in srv["palabra"]: srv["intentos"] -= 1
                        st.rerun()

    time.sleep(3)
    st.rerun()
