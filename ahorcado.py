import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Online Pro", layout="centered")

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

# --- LÓGICA DE COLOR PARA EL MUÑECO ---
def obtener_color_muneco(vidas):
    if vidas >= 5: return "#00FF00" # Verde
    if vidas >= 2: return "#FFFF00" # Amarillo
    return "#FF0000"                # Rojo

color_muneco = obtener_color_muneco(s["intentos"])

# --- CSS DEFINITIVO ---
fondo = "#0E1117" if s["tema"] == "oscuro" else "#FFFFFF"
texto = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"
btn_fondo = "#262730" if s["tema"] == "oscuro" else "#F0F2F6"
borde_color = "#444444" if s["tema"] == "oscuro" else "#CCCCCC"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {fondo}; color: {texto}; }}
    
    /* MUÑECO CON COLOR DINÁMICO Y ANCHO FIJO */
    .contenedor-dibujo {{
        display: flex;
        justify-content: center;
        margin: 10px 0;
    }}
    .dibujo-fijo {{
        background-color: #1a1a1a !important;
        color: {color_muneco} !important; /* COLOR VARIABLE */
        font-family: 'Courier New', monospace !important;
        font-size: 18px !important;
        line-height: 1.2 !important;
        padding: 15px !important;
        border: 3px solid {color_muneco}; /* El borde también cambia */
        border-radius: 12px;
        white-space: pre !important;
        display: block !important;
        width: 160px;
    }}

    /* PALABRA AUTO-AJUSTABLE */
    .palabra-display {{
        font-size: 8vw !important;
        font-weight: bold;
        color: #FFD700;
        text-align: center;
        letter-spacing: 2px;
        margin: 15px 0;
        white-space: nowrap;
    }}

    /* TECLADO 7 COLUMNAS */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 2px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    .stButton > button {{
        width: 100% !important;
        height: 45px !important;
        font-weight: bold !important;
        background-color: {btn_fondo} !important;
        color: {texto} !important;
        border: 2px solid {borde_color} !important; 
        border-radius: 8px !important;
    }}

    /* ESTILO NARANJA PARA EL BOTÓN DE CONFIRMAR ARRIESGAR */
    button[key*="confirmar"] {{
        border: 2px solid #FF8C00 !important;
        color: #FF8C00 !important;
    }}
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

# --- FLUJO DEL JUEGO ---
if not s["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 INICIAR"):
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
        # 1. DIBUJO CON COLOR DINÁMICO
        st.markdown(f'''
            <div class="contenedor-dibujo">
                <div class="dibujo-fijo">{get_dibujo(s["intentos"])}</div>
            </div>
            ''', unsafe_allow_html=True)

        # 2. VIDAS
        st.markdown(f"<div style='text-align:center; font-size:22px;'>❤️ Vidas: {s['intentos']}</div>", unsafe_allow_html=True)

        # 3. PALABRA
        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-display'>{visual}</div>", unsafe_allow_html=True)

        # 4. ARRIESGAR
        c1, c2 = st.columns([0.6, 0.4])
        with c2:
            if st.button("🔥 ARRIESGAR"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()
        
        if s["arriesgando"]:
            arr = st.text_input("Palabra completa:", key="inp_arr").lower().strip()
            if st.button("CONFIRMAR ENVÍO", key="confirmar"):
                if arr == s["palabra"]: s["gano_directo"] = True
                else: s.update({"intentos": 0, "arriesgando": False})
                st.rerun()

        # 5. TECLADO
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

        if st.button("🌓 Tema"):
            s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
            st.rerun()
        
        time.sleep(2)
        st.rerun()
