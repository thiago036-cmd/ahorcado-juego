import streamlit as st
import time

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

srv = obtener_servidor()

st.set_page_config(page_title="Ahorcado Pro", layout="centered")

# --- CSS DEFINITIVO PARA MÓVIL Y PC ---
st.markdown("""
    <style>
    /* Dibujo ASCII centrado y sin romperse */
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
        font-size: 20px;
    }

    /* Palabra oculta ajustable */
    .word-box { 
        font-size: 35px; letter-spacing: 8px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 15px; font-family: monospace;
    }

    /* Contenedor del teclado para que NO se duplique */
    .teclado-grid {
        display: flex;
        flex-wrap: wrap;
        justify-content: center;
        gap: 8px;
        margin-top: 20px;
    }

    /* Ajuste de botones para que parezcan teclado de móvil */
    .stButton > button {
        min-width: 45px !important;
        height: 45px !important;
        padding: 5px !important;
        font-weight: bold !important;
    }

    @media (max-width: 600px) {
        .word-box { font-size: 25px; letter-spacing: 5px; }
        .dibujo-box { font-size: 16px; }
    }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo(i):
    # Texto puro para evitar que se mueva
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

# --- FLUJO ---
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
            srv.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    # JUEGO ACTIVO
    st.markdown(f'<div class="dibujo-box">{obtener_dibujo(srv["intentos"])}</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    col1.metric("Vidas", srv["intentos"])
    with col2:
        adivina = st.text_input("¿La sabes?", key="full").lower().strip()
        if st.button("ADIVINAR"):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # TECLADO CORREGIDO: Usamos columnas pero controladas para que no se dupliquen
    st.write("### Selecciona una letra:")
    abc = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    
    # Creamos filas de 7 letras para que no se vea como una hilera infinita
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
