import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Ahorcado Online Pro", layout="centered")

@st.cache_resource
def engine():
    return {
        "p": "", "u": [], "v": 6, "win": False, "bet": False,
        "theme": "Claro"  # Estado del modo de color
    }

s = engine()
st_autorefresh(interval=2500, key="global_sync")

# --- 2. SELECTOR DE MODO (INTERFAZ) ---
with st.sidebar:
    st.title("⚙️ Ajustes")
    s["theme"] = st.radio("Modo de Pantalla", ["Claro", "Oscuro"], index=0 if s["theme"] == "Claro" else 1)
    if st.button("Reiniciar Aplicación"):
        s.update({"p": "", "u": [], "v": 6, "win": False, "bet": False})
        st.rerun()

# --- 3. DISEÑO UI (DINÁMICO SEGÚN MODO) ---
if s["theme"] == "Oscuro":
    bg_app = "#0f172a"
    bg_card = "#1e293b"
    text_main = "#f1f5f9"
    text_sec = "#94a3b8"
    border_col = "#334155"
    key_bg = "#1e293b"
    btn_bg = "#334155"
else:
    bg_app = "#f3f4f6"
    bg_card = "#ffffff"
    text_main = "#1f2937"
    text_sec = "#6b7280"
    border_col = "#e5e7eb"
    key_bg = "#f9fafb"
    btn_bg = "#ffffff"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&family=JetBrains+Mono&display=swap');
    
    .stApp {{ background-color: {bg_app}; color: {text_main}; font-family: 'Quicksand', sans-serif; transition: 0.3s; }}
    
    /* CABECERA */
    .title {{ text-align: center; font-weight: 700; font-size: 1.8rem; color: #7c3aed; margin-bottom: 10px; }}

    /* CONTENEDOR DEL MUÑECO (ARREGLADO) */
    .hangman-display {{
        background: #000000; /* Fondo negro siempre para el muñeco */
        border: 4px solid #7c3aed; border-radius: 15px;
        padding: 15px; width: 140px; margin: 0 auto 15px auto;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
    }}
    .ascii-art {{
        font-family: 'JetBrains Mono', monospace !important;
        font-size: 16px !important; line-height: 1.2 !important;
        color: #10b981; white-space: pre !important; text-align: left;
        display: inline-block;
    }}

    /* TARJETA DE JUEGO */
    .game-card {{
        background: {bg_card}; border-radius: 20px; padding: 20px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        border: 1px solid {border_col}; margin-bottom: 15px;
    }}

    /* PALABRA */
    .word-display {{ display: flex; justify-content: center; gap: 10px; margin: 20px 0; }}
    .letter-slot {{
        font-size: 26px; font-weight: 700; border-bottom: 3px solid #ddd6fe;
        width: 30px; text-align: center; color: #7c3aed; height: 35px;
    }}

    /* TECLADO UNIFICADO */
    .keyboard-box {{
        background: {key_bg}; padding: 15px; border-radius: 20px;
        display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px;
        border: 2px solid {border_col};
    }}

    /* BOTONES */
    div[data-testid="column"] button {{
        background: {btn_bg} !important; border: 1px solid {border_col} !important;
        color: {text_main} !important; border-radius: 10px !important;
        height: 44px !important; font-weight: 700 !important;
        box-shadow: 0 2px 0 {border_col} !important;
    }}
    div[data-testid="column"] button:hover {{
        background: #ddd6fe !important; color: #4c1d95 !important;
    }}

    .stButton > button[key*="btn-arr"] {{
        background: #fef3c7 !important; color: #d97706 !important;
        border: 1px solid #fde68a !important; font-weight: 700 !important;
    }}

    #MainMenu, footer, header {{ visibility: hidden; }}
    </style>
    """, unsafe_allow_html=True)

def get_drawing(v):
    stages = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
    ]
    return stages[v]

# --- 4. LÓGICA DE INTERFAZ ---
if not s["p"]:
    st.markdown("<div class='title'>AHORCADO ONLINE</div>", unsafe_allow_html=True)
    with st.container():
        p_input = st.text_input("Ingresa la palabra secreta:", type="password")
        if st.button("COMENZAR PARTIDA", use_container_width=True):
            if p_input:
                s.update({"p": p_input.lower().strip(), "u": [], "v": 6, "win": False})
                st.rerun()
else:
    win = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    
    if win or s["v"] <= 0:
        st.markdown(f"<div class='game-card' style='text-align:center;'>", unsafe_allow_html=True)
        if win:
            st.balloons()
            st.markdown("<h2 style='color:#10b981;'>✨ ¡GANASTE! ✨</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#ef4444;'>GAME OVER</h2>", unsafe_allow_html=True)
        st.markdown(f"La palabra era: <b style='color:#7c3aed; font-size:24px;'>{s['p'].upper()}</b>", unsafe_allow_html=True)
        if st.button("VOLVER A JUGAR", use_container_width=True):
            s.update({"p": "", "u": [], "v": 6, "win": False, "bet": False})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='title'>AHORCADO ONLINE</div>", unsafe_allow_html=True)
        
        # Área Visual
        st.markdown(f"""
            <div class='game-card' style='text-align:center;'>
                <div class='hangman-display'>
                    <div class='ascii-art'>{get_drawing(s['v'])}</div>
                </div>
                <div style='color:#9ca3af; font-size:12px; font-weight:700;'>INTENTOS: {s['v']} / 6</div>
                <div class='word-display'>
                    {"".join([f"<div class='letter-slot'>{l.upper() if l in s['u'] or l == ' ' else ''}</div>" for l in s['p']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Teclado
        st.markdown("<div class='keyboard-box'>", unsafe_allow_html=True)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["u"]:
                    color_l = "#10b981" if l_min in s["p"] else "#94a3b8"
                    st.markdown(f"<div style='text-align:center; color:{color_l}; font-weight:900; height:44px; line-height:44px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"btn-{letra}"):
                        s["u"].append(l_min)
                        if l_min not in s["p"]: s["v"] -= 1
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Arriesgar
        st.markdown("<br>", unsafe_allow_html=True)
        izq, der = st.columns([0.6, 0.4])
        with der:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["bet"] = not s["bet"]
                st.rerun()

        if s["bet"]:
            ans = st.text_input("Escribe la palabra:", key="ans").lower().strip()
            if st.button("ENVIAR", use_container_width=True):
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
