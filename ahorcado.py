import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN DE ALTO NIVEL ---
st.set_page_config(page_title="Ahorcado Online", layout="centered")

@st.cache_resource
def obtener_motor_global():
    return {"palabra": "", "usadas": [], "vidas": 6, "victoria": False, "arriesgando": False}

s = obtener_motor_global()
# Sincronización automática cada 2.5 segundos para juego cooperativo
st_autorefresh(interval=2500, key="sync_global")

# --- 2. DISEÑO UI PREMIUM ---
color_estado = "#10b981" if s["vidas"] >= 4 else "#f59e0b" if s["vidas"] >= 2 else "#ef4444"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono&display=swap');
    
    .stApp {{ background: radial-gradient(circle at top, #1e293b, #0f172a); color: #f8fafc; font-family: 'Inter', sans-serif; }}
    
    /* CABECERA */
    .header-title {{
        text-align: center; font-weight: 900; font-size: 2.5rem;
        background: linear-gradient(to right, #38bdf8, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 20px; letter-spacing: -1px;
    }}

    /* TARJETA DEL DIBUJO */
    .card-ahorcado {{
        background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(12px); border-radius: 24px; padding: 20px;
        width: 140px; margin: 0 auto 15px auto; box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }}
    .arte-ascii {{
        font-family: 'JetBrains Mono', monospace; font-size: 14px;
        color: {color_estado}; line-height: 1.1; white-space: pre; text-align: left;
    }}

    /* BADGE DE VIDAS */
    .status-badge {{
        background: {color_estado}22; color: {color_estado}; padding: 5px 15px;
        border-radius: 100px; font-weight: 700; font-size: 13px;
        border: 1px solid {color_estado}44; width: fit-content; margin: 0 auto 20px auto;
    }}

    /* PALABRA */
    .palabra-display {{
        font-family: 'JetBrains Mono', monospace; font-size: 36px; font-weight: 900;
        letter-spacing: 10px; color: #ffffff; text-align: center; margin: 25px 0;
    }}

    /* BOTONES DEL TECLADO */
    div[data-testid="column"] button {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important; border-radius: 12px !important;
        height: 45px !important; font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="column"] button:hover {{
        border-color: #38bdf8 !important; color: #38bdf8 !important;
        transform: translateY(-2px); background: rgba(56, 189, 248, 0.1) !important;
    }}

    /* BOTÓN ARRIESGAR */
    .stButton > button[key*="btn-arr"] {{
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: white !important; border: none !important;
        box-shadow: 0 10px 20px rgba(217, 119, 6, 0.3) !important;
        border-radius: 14px !important;
    }}

    /* LIMPIEZA INTERFAZ */
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo(v):
    etapas = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
    ]
    return etapas[v]

# --- 3. FLUJO DEL JUEGO ---
if not s["palabra"]:
    st.markdown("<h1 class='header-title'>AHORCADO ONLINE</h1>", unsafe_allow_html=True)
    with st.container():
        input_p = st.text_input("PALABRA SECRETA", type="password", help="Escribe la palabra para que otros adivinen")
        if st.button("CREAR SALA", use_container_width=True):
            if input_p:
                s.update({"palabra": input_p.lower().strip(), "usadas": [], "vidas": 6, "victoria": False})
                st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["victoria"]
    
    if ganado or s["vidas"] <= 0:
        st.markdown("<br><br>", unsafe_allow_html=True)
        if ganado:
            st.balloons()
            st.markdown("<h2 style='color:#10b981; text-align:center;'>¡VICTORIA!</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#ef4444; text-align:center;'>FIN DEL JUEGO</h2>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='text-align:center; font-size:20px;'>La palabra era: <b>{s['palabra'].upper()}</b></p>", unsafe_allow_html=True)
        if st.button("NUEVA PARTIDA", use_container_width=True):
            s.update({"palabra": "", "usadas": [], "vidas": 6, "victoria": False, "arriesgando": False})
            st.rerun()
    else:
        # Pantalla Principal
        st.markdown(f"""
            <div class='header-title' style='font-size:1.5rem; margin-bottom:10px;'>AHORCADO ONLINE</div>
            <div class='card-ahorcado'><div class='arte-ascii'>{obtener_dibujo(s['vidas'])}</div></div>
            <div class='status-badge'>INTENTOS: {s['vidas']} / 6</div>
            """, unsafe_allow_html=True)

        visual = "".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-display'>{visual}</div>", unsafe_allow_html=True)

        # Teclado Pro
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["usadas"]:
                    color_l = "#10b981" if l_min in s["palabra"] else "#475569"
                    st.markdown(f"<div style='text-align:center; color:{color_l}; font-weight:900; height:45px; line-height:45px; font-size:18px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"btn-{letra}"):
                        s["usadas"].append(l_min)
                        if l_min not in s["palabra"]: s["vidas"] -= 1
                        st.rerun()

        # Botón Arriesgar
        st.markdown("<br>", unsafe_allow_html=True)
        izq, der = st.columns([0.6, 0.4])
        with der:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()

        if s["arriesgando"]:
            intento = st.text_input("¿CUÁL ES LA PALABRA?", key="input_final").lower().strip()
            if st.button("ENVIAR RESPUESTA", use_container_width=True):
                if intento == s["palabra"]: s["victoria"] = True
                else: s["vidas"] = 0
                st.rerun()
