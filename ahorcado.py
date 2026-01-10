import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Online Pro", layout="centered")

# --- CEREBRO ONLINE (COMPARTIDO POR TODOS) ---
@st.cache_resource
def obtener_juego():
    return {
        "palabra": "", 
        "usadas": [], 
        "intentos": 6, 
        "gano_directo": False,
        "tema": "oscuro",
        "arriesgando": False  # Controla si se muestra el input de arriesgar
    }

s = obtener_juego()

# --- CSS: VERTICALIDAD, BORDES Y BOTÓN ARRIESGAR ---
fondo = "#0E1117" if s["tema"] == "oscuro" else "#FFFFFF"
texto = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"
btn_fondo = "#262730" if s["tema"] == "oscuro" else "#F0F2F6"
borde_color = "#444444" if s["tema"] == "oscuro" else "#CCCCCC"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {fondo}; color: {texto}; }}
    
    /* FUERZA 7 COLUMNAS HORIZONTALES EN EL TECLADO */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 4px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    /* ESTILO BOTONES GENERALES (BORDES GRUESOS) */
    .stButton > button {{
        width: 100% !important;
        height: 55px !important;
        font-weight: bold !important;
        background-color: {btn_fondo} !important;
        color: {texto} !important;
        border: 3px solid {borde_color} !important; 
        border-radius: 10px !important;
    }}

    /* DISEÑO VERTICAL CENTRADO */
    .centrar {{ display: flex; justify-content: center; margin-bottom: 10px; }}
    .vidas-box {{ font-size: 24px; font-weight: bold; color: #FF4B4B; text-align: center; }}
    .palabra-box {{ font-size: 35px; font-weight: bold; color: #FFD700; text-align: center; letter-spacing: 8px; margin: 20px 0; font-family: monospace; }}
    
    pre {{ background-color: #111 !important; color: #00FF00 !important; font-size: 18px !important; border: 2px solid #555; width: fit-content; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False})
    st.rerun()

def dibujo(i):
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

# --- LÓGICA DE PANTALLAS ---
if not s["palabra"]:
    st.title("🏹 Sala Online")
    # Botón de tema arriba a la derecha
    if st.button("🌓 Tema"):
        s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
        st.rerun()
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR PARTIDA"):
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
        st.error(f"💀 DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # 1. DIBUJO
        st.markdown(f'<div class="centrar"><pre>{dibujo(s["intentos"])}</pre></div>', unsafe_allow_html=True)

        # 2. VIDAS
        st.markdown(f"<div class='vidas-box'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)

        # 3. PALABRA SECRETA
        txt = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-box'>{txt}</div>", unsafe_allow_html=True)

        # 4. BOTÓN ARRIESGAR (Abajo a la derecha)
        col_espacio, col_arriesgar = st.columns([0.6, 0.4])
        with col_arriesgar:
            if st.button("🔥 ARRIESGAR"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()
        
        if s["arriesgando"]:
            adv = st.text_input("Escribe la palabra completa:", key="adv_box").lower().strip()
            if st.button("CONFIRMAR ARRIESGAR"):
                if adv == s["palabra"]: s["gano_directo"] = True
                else: s.update({"intentos": 0, "arriesgando": False})
                st.rerun()

        # 5. TECLADO HORIZONTAL
        st.write("Selecciona una letra:")
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
                        if st.button(letra, key=f"k-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()
        
        # 6. MODO TEMA (FLOTANTE)
        if st.button("🌓 Tema"):
            s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
            st.rerun()

        time.sleep(2)
        st.rerun()
