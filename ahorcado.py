import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Online Final", layout="centered")

# --- CEREBRO ONLINE ---
@st.cache_resource
def obtener_juego():
    return {
        "palabra": "", 
        "usadas": [], 
        "intentos": 6, 
        "gano_directo": False,
        "tema": "oscuro",
        "arriesgando": False
    }

s = obtener_juego()

# --- CSS DEFINITIVO (BLINDADO PARA MÓVIL) ---
fondo = "#0E1117" if s["tema"] == "oscuro" else "#FFFFFF"
texto = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"
btn_fondo = "#262730" if s["tema"] == "oscuro" else "#F0F2F6"
borde_color = "#444444" if s["tema"] == "oscuro" else "#CCCCCC"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {fondo}; color: {texto}; }}
    
    /* TECLADO 7 COLUMNAS */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 3px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    /* BOTONES GENERALES */
    .stButton > button {{
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
        background-color: {btn_fondo} !important;
        color: {texto} !important;
        border: 3px solid {borde_color} !important; 
        border-radius: 10px !important;
    }}

    /* BOTÓN ARRIESGAR (CSS MANUAL PARA EVITAR ERROR) */
    div.stButton > button:contains("ARRIESGAR") {{
        border: 3px solid #FF8C00 !important;
        color: #FF8C00 !important;
    }}

    /* EL DIBUJO NO SE DESARMA */
    .dibujo-container {{
        text-align: center;
        background-color: #111;
        padding: 15px;
        border-radius: 15px;
        border: 2px solid {borde_color};
        display: inline-block;
        margin: 0 auto;
    }}

    pre {{
        color: #00FF00 !important;
        font-size: 18px !important;
        line-height: 1.2 !important;
        margin: 0 !important;
        font-family: 'Courier New', monospace !important;
    }}

    /* PALABRA QUE SIEMPRE CABE (TAMAÑO DINÁMICO) */
    .palabra-display {{
        font-size: 8vw !important; /* Tamaño basado en el ancho de la pantalla */
        max-font-size: 40px;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        letter-spacing: 2px;
        margin: 20px 0;
        white-space: nowrap;
    }}

    .vidas-box {{ font-size: 24px; font-weight: bold; color: #FF4B4B; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False})
    st.rerun()

def get_dibujo(i):
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

# --- LÓGICA DE PARTIDA ---
if not s["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Configura la palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR JUEGO"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado:
        st.balloons()
        st.success(f"🏆 ¡VICTORIA! ERA: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar)
    elif s["intentos"] <= 0:
        st.error(f"💀 PERDIMOS. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # 1. DIBUJO (FIJO)
        st.markdown(f'<div style="text-align:center"><div class="dibujo-container"><pre>{get_dibujo(s["intentos"])}</pre></div></div>', unsafe_allow_html=True)

        # 2. VIDAS
        st.markdown(f"<div class='vidas-box'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)

        # 3. PALABRA ELÁSTICA
        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-display'>{visual}</div>", unsafe_allow_html=True)

        # 4. ARRIESGAR (ARRIBA DEL TECLADO)
        col1, col2 = st.columns([0.5, 0.5])
        with col2:
            if st.button("🔥 ARRIESGAR"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()
        
        if s["arriesgando"]:
            arriesgo = st.text_input("Escribe la palabra completa:", key="box_arriesgar").lower().strip()
            if st.button("CONFIRMAR ENVÍO"):
                if arriesgo == s["palabra"]: s["gano_directo"] = True
                else: s.update({"intentos": 0, "arriesgando": False})
                st.rerun()

        # 5. TECLADO
        st.write("Letras:")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            fila = abc[i:i+7]
            cols = st.columns(7)
            for j, letra in enumerate(fila):
                l_min = letra.lower()
                with cols[j]:
                    if l_min in s["usadas"]:
                        st.write("✅" if l_min in s["palabra"] else "❌")
                    else:
                        if st.button(letra, key=f"btn-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()

        # TEMA Y REFRESH
        if st.button("🌓 Tema"):
            s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
            st.rerun()
        
        time.sleep(2)
        st.rerun()
