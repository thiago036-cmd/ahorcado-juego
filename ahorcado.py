import streamlit as st
import time

# --- CONFIGURACIÓN E INTERFAZ ---
st.set_page_config(page_title="Ahorcado Pro Online", layout="centered")

# MEMORIA COMPARTIDA (ONLINE REALTIME)
@st.cache_resource
def obtener_estado():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "tema": "oscuro"}

s = obtener_estado()

# SELECTOR DE TEMA
col_tema = st.columns([0.8, 0.2])
with col_tema[1]:
    if st.button("🌓"):
        s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
        st.rerun()

# --- CSS BLINDADO PARA MÓVIL (TECLADO FIJO Y LETRAS VISIBLES) ---
bg = "#0E1117" if s["tema"] == "oscuro" else "#F0F2F6"
txt = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"
btn_bg = "#262730" if s["tema"] == "oscuro" else "#FFFFFF"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bg}; color: {txt}; }}
    
    /* FUERZA 7 COLUMNAS EN MÓVIL (EVITA EL APILADO VERTICAL) */
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

    /* BOTONES DEL TECLADO: SIEMPRE CENTRADOS Y VISIBLES */
    .stButton > button {{
        width: 100% !important;
        height: 45px !important;
        padding: 0px !important;
        font-size: 16px !important;
        font-weight: bold !important;
        background-color: {btn_bg} !important;
        color: {txt} !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        border: 1px solid #444 !important;
    }}

    .palabra-caja {{ font-size: 32px; font-weight: bold; color: #FFD700; text-align: center; letter-spacing: 6px; margin: 15px 0; }}
    .vidas-caja {{ font-size: 22px; font-weight: bold; color: #FF4B4B; text-align: center; }}
    pre {{ background-color: #111 !important; color: #00FF00 !important; font-size: 16px !important; line-height: 1; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

def dibujo(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\  | \n/ \  | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|\  | \n/    | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|\  | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======",
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n=======" 
    ]
    return etapas[i]

# --- LÓGICA DE JUEGO ---
if not s["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta para todos:", type="password")
    if st.button("🚀 INICIAR"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    if ganado:
        st.balloons()
        st.success(f"🏆 ¡VICTORIA! PALABRA: {s['palabra'].upper()}")
        st.button("🔄 OTRA PARTIDA", on_click=reiniciar)
    elif s["intentos"] <= 0:
        st.error(f"💀 DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # PANTALLA DE JUEGO
        st.markdown(f"<div class='vidas-caja'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)
        
        c_dib, c_adv = st.columns(2)
        with c_dib: 
            st.code(dibujo(s["intentos"]))
        with c_adv:
            adv = st.text_input("🎯 ¿La sabes?", key="adv_box").lower().strip()
            if st.button("ENVIAR"):
                if adv == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()

        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-caja'>{visual}</div>", unsafe_allow_html=True)

        # TECLADO FIJO (7 COLUMNAS)
        st.write("Selecciona letra:")
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
        
        # SINCRONIZACIÓN AUTOMÁTICA
        time.sleep(2)
        st.rerun()
