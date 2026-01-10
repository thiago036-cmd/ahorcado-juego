import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN DE ÉLITE ---
st.set_page_config(page_title="Ahorcado online", layout="centered", initial_sidebar_state="collapsed")

@st.cache_resource
def get_global_engine():
    return {"word": "", "used": [], "lives": 6, "win": False, "betting": False}

s = get_global_engine()
st_autorefresh(interval=2500, key="engine_sync")

# --- 2. MOTOR ESTÉTICO (CSS CUSTOM) ---
lives_color = "#10b981" if s["lives"] >= 4 else "#f59e0b" if s["lives"] >= 2 else "#ef4444"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700;900&family=JetBrains+Mono&display=swap');
    
    .stApp {{ background: radial-gradient(circle at top, #1e293b, #0f172a); color: #f8fafc; font-family: 'Inter', sans-serif; }}
    
    /* CONTENEDOR PRINCIPAL */
    .main-game-container {{ display: flex; flex-direction: column; align-items: center; padding-top: 20px; }}

    /* CANVAS DEL AHORCADO */
    .hangman-card {{
        background: rgba(30, 41, 59, 0.7); border: 1px solid rgba(255,255,255,0.1);
        backdrop-filter: blur(10px); border-radius: 24px; padding: 20px;
        width: 140px; margin-bottom: 15px; box-shadow: 0 20px 50px rgba(0,0,0,0.3);
    }}
    .hangman-art {{
        font-family: 'JetBrains Mono', monospace; font-size: 14px;
        color: {lives_color}; line-height: 1.1; white-space: pre; text-align: left;
    }}

    /* INDICADOR DE VIDAS */
    .lives-badge {{
        background: {lives_color}22; color: {lives_color}; padding: 4px 12px;
        border-radius: 100px; font-weight: 700; font-size: 14px; margin-bottom: 20px;
        border: 1px solid {lives_color}44;
    }}

    /* PALABRA SECRETA */
    .word-slot {{
        font-family: 'JetBrains Mono', monospace; font-size: 32px; font-weight: 900;
        letter-spacing: 8px; color: #ffffff; text-align: center; margin: 25px 0;
        text-shadow: 0 0 20px rgba(255,255,255,0.2);
    }}

    /* TECLADO GAMER */
    div[data-testid="column"] button {{
        background: rgba(255, 255, 255, 0.05) !important;
        border: 1px solid rgba(255, 255, 255, 0.1) !important;
        color: #94a3b8 !important; border-radius: 12px !important;
        height: 42px !important; font-weight: 700 !important;
        transition: all 0.2s ease !important;
    }}
    div[data-testid="column"] button:hover {{
        background: rgba(255, 255, 255, 0.1) !important;
        border-color: #38bdf8 !important; color: #38bdf8 !important;
        transform: translateY(-2px);
    }}

    /* BOTÓN ARRIESGAR (PREMIUM) */
    .stButton > button[key*="btn-arr"] {{
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        color: white !important; border: none !important;
        box-shadow: 0 10px 20px rgba(217, 119, 6, 0.3) !important;
        width: 100% !important; border-radius: 14px !important;
    }}

    /* OCULTAR ELEMENTOS INNECESARIOS */
    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

def draw_art(lives):
    stages = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
    ]
    return stages[lives]

# --- 3. LÓGICA DE JUEGO ---
if not s["word"]:
    st.markdown("<h1 style='text-align:center;'>HANGMAN <span style='color:#38bdf8;'>ELITE</span></h1>", unsafe_allow_html=True)
    with st.container():
        word_input = st.text_input("CONFIGURAR PALABRA SECRETA", type="password", help="Solo tú sabes esto al inicio")
        if st.button("CREAR PARTIDA", use_container_width=True):
            if word_input:
                s.update({"word": word_input.lower().strip(), "used": [], "lives": 6, "win": False})
                st.rerun()
else:
    is_win = all(l in s["used"] or l == " " for l in s["word"]) or s["win"]
    
    if is_win or s["lives"] <= 0:
        st.markdown("<div class='main-game-container'>", unsafe_allow_html=True)
        if is_win:
            st.balloons()
            st.markdown(f"<h2 style='color:#10b981; text-align:center;'>VICTORIA TOTAL</h2>", unsafe_allow_html=True)
        else:
            st.markdown(f"<h2 style='color:#ef4444; text-align:center;'>MISIÓN FALLIDA</h2>", unsafe_allow_html=True)
        
        st.markdown(f"<p style='text-align:center;'>LA PALABRA ERA: <b>{s['word'].upper()}</b></p>", unsafe_allow_html=True)
        if st.button("REINICIAR SESIÓN", use_container_width=True):
            s.update({"word": "", "used": [], "lives": 6, "win": False, "betting": False})
            st.rerun()
    else:
        # PANTALLA DE JUEGO
        st.markdown(f"""
            <div class='main-game-container'>
                <div class='hangman-card'><div class='hangman-art'>{draw_art(s['lives'])}</div></div>
                <div class='lives-badge'>STAMINA: {s['lives']} / 6</div>
            </div>
            """, unsafe_allow_html=True)

        display_word = "".join([l.upper() if l in s["used"] or l == " " else "_" for l in s["word"]])
        st.markdown(f"<div class='word-slot'>{display_word}</div>", unsafe_allow_html=True)

        # TECLADO TÁCTIL (Grid de 7 columnas optimizado para móviles)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, char in enumerate(abc):
            low_char = char.lower()
            with cols[i % 7]:
                if low_char in s["used"]:
                    char_color = "#10b981" if low_char in s["word"] else "#475569"
                    st.markdown(f"<div style='text-align:center; color:{char_color}; font-weight:900; height:42px; line-height:42px; font-size:18px;'>{char}</div>", unsafe_allow_html=True)
                else:
                    if st.button(char, key=f"btn-{char}"):
                        s["used"].append(low_char)
                        if low_char not in s["word"]: s["lives"] -= 1
                        st.rerun()

        # ÁREA DE ARRIESGAR (Abajo a la derecha)
        st.markdown("<br>", unsafe_allow_html=True)
        c_left, c_right = st.columns([0.6, 0.4])
        with c_right:
            if st.button("🔥 ARRIESGAR TODO", key="btn-arr"):
                s["betting"] = not s["betting"]
                st.rerun()

        if s["betting"]:
            final_guess = st.text_input("INTRODUCE LA PALABRA FINAL:", key="final_input").lower().strip()
            if st.button("CONFIRMAR ENVÍO", use_container_width=True):
                if final_guess == s["word"]: s["win"] = True
                else: s["lives"] = 0
                st.rerun()

