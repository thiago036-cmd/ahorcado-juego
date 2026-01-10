import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Ahorcado Pro Online", layout="centered")

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

# --- LÓGICA DE COLOR DINÁMICO ---
def color_alerta(vidas):
    if vidas >= 5: return "#00ff88" # Verde Neón
    if vidas >= 3: return "#ffcc00" # Amarillo Oro
    if vidas >= 2: return "#ff8800" # Naranja Alerta
    return "#ff4444"                # Rojo Sangre

c_muneco = color_alerta(s["intentos"])

# --- CSS DE ALTO IMPACTO ---
bg_main = "#0f172a" if s["tema"] == "oscuro" else "#f8fafc"
card_bg = "rgba(30, 41, 59, 0.7)" if s["tema"] == "oscuro" else "rgba(255, 255, 255, 0.9)"
text_main = "#f8fafc" if s["tema"] == "oscuro" else "#0f172a"
border_glow = c_muneco if s["palabra"] else "#38bdf8"

st.markdown(f"""
    <style>
    /* Fondo General */
    .stApp {{
        background: {bg_main};
        color: {text_main};
        font-family: 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
    }}

    /* Contenedor del Muñeco (Glassmorphism) */
    .glass-card {{
        background: {card_bg};
        backdrop-filter: blur(10px);
        border: 2px solid {c_muneco}44;
        border-radius: 24px;
        padding: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5), inset 0 0 15px {c_muneco}22;
        margin-bottom: 20px;
        display: flex;
        justify-content: center;
    }}

    pre {{
        color: {c_muneco} !important;
        text-shadow: 0 0 10px {c_muneco}aa;
        font-size: 1.2rem !important;
        line-height: 1.1 !important;
        background: transparent !important;
        border: none !important;
        margin: 0 !important;
    }}

    /* Palabra Secreta Estilo Letrero */
    .palabra-container {{
        font-size: 9vw !important;
        font-weight: 800;
        color: #fbbf24;
        text-shadow: 0 0 15px rgba(251, 191, 36, 0.4);
        text-align: center;
        letter-spacing: 5px;
        margin: 25px 0;
        text-transform: uppercase;
    }}

    /* Botones de Letras (Teclado) */
    div[data-testid="stHorizontalBlock"] button {{
        background: {card_bg} !important;
        border: 2px solid #334155 !important;
        color: {text_main} !important;
        border-radius: 12px !important;
        height: 50px !important;
        font-size: 1.1rem !important;
        transition: all 0.2s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }}

    div[data-testid="stHorizontalBlock"] button:hover {{
        border-color: #38bdf8 !important;
        transform: translateY(-2px);
        box-shadow: 0 0 15px rgba(56, 189, 248, 0.4) !important;
    }}

    /* Botón Arriesgar Pro */
    .stButton > button[key*="btn-arriesgar"] {{
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 15px !important;
        font-weight: bold !important;
        box-shadow: 0 4px 15px rgba(217, 119, 6, 0.4) !important;
    }}

    /* Símbolos de acierto/error */
    .status-icon {{ font-size: 1.5rem; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False})
    st.rerun()

def get_dibujo(i):
    etapas = [
        "  +---+ \n  |   | \n  O   | \n /|\\  | \n / \\  | \n      | \n=========",
        "  +---+ \n  |   | \n  O   | \n /|\\  | \n /    | \n      | \n=========",
        "  +---+ \n  |   | \n  O   | \n /|\\  | \n      | \n      | \n=========",
        "  +---+ \n  |   | \n  O   | \n /|   | \n      | \n      | \n=========",
        "  +---+ \n  |   | \n  O   | \n  |   | \n      | \n      | \n=========",
        "  +---+ \n  |   | \n  O   | \n      | \n      | \n      | \n=========",
        "  +---+ \n  |   | \n      | \n      | \n      | \n      | \n=========" 
    ]
    return etapas[i]

# --- LÓGICA DE INTERFAZ ---
if not s["palabra"]:
    st.markdown("<h1 style='text-align: center;'>🎯 Ahorcado</h1>", unsafe_allow_html=True)
    with st.container():
        st.markdown("<div style='padding: 20px; border-radius: 20px; background: rgba(255,255,255,0.05);'>", unsafe_allow_html=True)
        p = st.text_input("Ingresa la palabra para el desafío:", type="password", help="Los demás jugadores intentarán adivinarla")
        if st.button("🚀 CREAR SALA", use_container_width=True):
            if p:
                s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado:
        st.balloons()
        st.markdown(f"<h2 style='text-align:center; color:#00ff88;'>🏆 ¡VICTORIA MAGISTRAL!</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>La palabra era: <b>{s['palabra'].upper()}</b></p>", unsafe_allow_html=True)
        st.button("🔄 JUGAR OTRA VEZ", on_click=reiniciar, use_container_width=True)
    elif s["intentos"] <= 0:
        st.markdown(f"<h2 style='text-align:center; color:#ff4444;'>💀 FIN DEL JUEGO</h2>", unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center;'>Palabra oculta: <b>{s['palabra'].upper()}</b></p>", unsafe_allow_html=True)
        st.button("🔄 REINTENTAR", on_click=reiniciar, use_container_width=True)
    else:
        # 1. TARJETA DEL MUÑECO
        st.markdown(f'<div class="glass-card"><pre>{get_dibujo(s["intentos"])}</pre></div>', unsafe_allow_html=True)

        # 2. STATUS BAR
        c_vidas, c_tema = st.columns([0.8, 0.2])
        with c_vidas:
            st.markdown(f"<div style='font-size:1.5rem;'>❤️ <b>{s['intentos']}</b> vidas restantes</div>", unsafe_allow_html=True)
        with c_tema:
            if st.button("🌓"):
                s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
                st.rerun()

        # 3. PALABRA ELÁSTICA
        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-container'>{visual}</div>", unsafe_allow_html=True)

        # 4. SECCIÓN ARRIESGAR
        col_empty, col_arr = st.columns([0.6, 0.4])
        with col_arr:
            if st.button("🔥 ARRIESGAR TODO", key="btn-arriesgar", use_container_width=True):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()
        
        if s["arriesgando"]:
            with st.container():
                arr = st.text_input("Escribe la palabra completa:", key="f_arr").lower().strip()
                if st.button("CONFIRMAR ENVÍO", key="btn-confirm", use_container_width=True):
                    if arr == s["palabra"]: s["gano_directo"] = True
                    else: s.update({"intentos": 0, "arriesgando": False})
                    st.rerun()

        # 5. TECLADO ESTILIZADO
        st.markdown("<p style='opacity:0.6; margin-top:20px;'>TECLADO VIRTUAL</p>", unsafe_allow_html=True)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            fila = abc[i:i+7]
            cols = st.columns(7)
            for j, letra in enumerate(fila):
                l_min = letra.lower()
                with cols[j]:
                    if l_min in s["usadas"]:
                        st.markdown(f"<div class='status-icon'>{'✅' if l_min in s['palabra'] else '❌'}</div>", unsafe_allow_html=True)
                    else:
                        if st.button(letra, key=f"k-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()
        
        # Sincronización Online
        time.sleep(2)
        st.rerun()

