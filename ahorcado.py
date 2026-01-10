import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Ahorcado Online Pro", layout="centered")

@st.cache_resource
def engine():
    return {"p": "", "u": [], "v": 6, "win": False, "bet": False}

s = engine()
st_autorefresh(interval=2500, key="global_sync")

# --- 2. UI/UX DESIGN SYSTEM (COMPACTO Y PROFESIONAL) ---
accent = "#22d3ee" if s["v"] >= 4 else "#fbbf24" if s["v"] >= 2 else "#f87171"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;700;800&family=JetBrains+Mono&display=swap');
    
    .stApp {{ background: #020617; color: #f8fafc; font-family: 'Plus Jakarta Sans', sans-serif; }}
    
    /* CABECERA COMPACTA */
    .title {{
        text-align: center; font-weight: 800; font-size: 1.8rem;
        background: linear-gradient(135deg, #22d3ee, #818cf8);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 10px;
    }}

    /* CONTENEDOR DE JUEGO */
    .game-card {{
        background: #0f172a; border: 1px solid #1e293b; border-radius: 20px;
        padding: 15px; margin-bottom: 15px; box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }}

    /* ARTE ASCII COMPACTO */
    .ascii-box {{
        font-family: 'JetBrains Mono', monospace; font-size: 12px;
        color: {accent}; line-height: 1; white-space: pre; 
        display: flex; justify-content: center; margin-bottom: 10px;
    }}

    /* PALABRA EN CAJAS */
    .word-display {{
        display: flex; justify-content: center; gap: 8px; margin: 15px 0;
    }}
    .letter-slot {{
        font-family: 'JetBrains Mono', monospace; font-size: 24px; font-weight: 800;
        border-bottom: 3px solid #334155; width: 30px; text-align: center; color: #fff;
    }}

    /* TECLADO UNIDO (EL FONDO QUE PEDISTE) */
    .keyboard-bg {{
        background: #1e293b; padding: 12px; border-radius: 16px;
        display: grid; grid-template-columns: repeat(7, 1fr); gap: 6px;
        border: 1px solid #334155;
    }}

    /* BOTONES ESTILO KEYCAP */
    div[data-testid="column"] button {{
        background: #334155 !important; border: none !important;
        color: #f8fafc !important; border-radius: 8px !important;
        height: 40px !important; font-weight: 700 !important;
        font-size: 14px !important; transition: 0.2s !important;
    }}
    div[data-testid="column"] button:hover {{
        background: {accent} !important; color: #020617 !important;
        transform: scale(1.05);
    }}

    /* BOTÓN ARRIESGAR DERECHA */
    .btn-bet-container {{ display: flex; justify-content: flex-end; margin-top: 15px; }}
    .stButton > button[key*="btn-arr"] {{
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: white !important; border: none !important;
        width: 120px !important; font-size: 12px !important;
    }}

    /* ELIMINAR ESPACIOS DE STREAMLIT */
    .block-container {{ padding-top: 2rem !important; }}
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

def draw(v):
    stages = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=====",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n====="
    ]
    return stages[v]

# --- 3. LÓGICA DE INTERFAZ ---
if not s["p"]:
    st.markdown("<div class='title'>AHORCADO ONLINE</div>", unsafe_allow_html=True)
    with st.form("setup"):
        p_input = st.text_input("PALABRA SECRETA", type="password")
        if st.form_submit_button("CREAR PARTIDA", use_container_width=True):
            if p_input:
                s.update({"p": p_input.lower().strip(), "u": [], "v": 6, "win": False})
                st.rerun()
else:
    win = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    
    if win or s["v"] <= 0:
        st.markdown("<div class='game-card' style='text-align:center;'>", unsafe_allow_html=True)
        if win:
            st.balloons()
            st.markdown(f"<h2 style='color:#22d3ee;'>¡VICTORIA!</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='color:#f87171;'>JUEGO TERMINADO</h2>", unsafe_allow_html=True)
        st.markdown(f"LA PALABRA ERA: <b>{s['p'].upper()}</b>", unsafe_allow_html=True)
        if st.button("NUEVA PARTIDA", use_container_width=True):
            s.update({"p": "", "u": [], "v": 6, "win": False, "bet": False})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Pantalla de Juego Compacta
        st.markdown(f"<div class='title'>AHORCADO ONLINE</div>", unsafe_allow_html=True)
        st.markdown(f"""
            <div class='game-card'>
                <div class='ascii-box'>{draw(s['v'])}</div>
                <div style='text-align:center; font-size:12px; color:#94a3b8; font-weight:700;'>
                    VIDAS: {s['v']} / 6
                </div>
                <div class='word-display'>
                    {"".join([f"<div class='letter-slot'>{l.upper() if l in s['u'] or l == ' ' else ''}</div>" for l in s['p']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Teclado en fondo unido
        st.markdown("<div class='keyboard-bg'>", unsafe_allow_html=True)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["u"]:
                    color_l = "#22d3ee" if l_min in s["p"] else "#475569"
                    st.markdown(f"<div style='text-align:center; color:{color_l}; font-weight:900; height:40px; line-height:40px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"btn-{letra}"):
                        s["u"].append(l_min)
                        if l_min not in s["p"]: s["v"] -= 1
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Arriesgar
        st.markdown("<div class='btn-bet-container'>", unsafe_allow_html=True)
        c1, c2 = st.columns([0.6, 0.4])
        with c2:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["bet"] = not s["bet"]
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if s["bet"]:
            ans = st.text_input("SOLUCIÓN:", key="ans").lower().strip()
            if st.button("ENVIAR", use_container_width=True):
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
