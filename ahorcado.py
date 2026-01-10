import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO UI (TECLADO STICKER Y VERTICALIDAD)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")

# Estilo de letras: Blanco con borde negro (Modo Claro)
txt_style = "color: white; -webkit-text-stroke: 1.5px black; font-weight: 900;" if not s["dark"] else f"color: {tx}; font-weight: 700;"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: 'Segoe UI', sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%; }}
    .card {{ background:{cd}; border:2px solid {br}; border-radius:20px; padding:25px; width: 100%; margin-bottom: 20px; }}
    
    /* MUÑECO REPARADO (ESTABLE) */
    .hangman-box {{ 
        font-family: 'Courier New', monospace; font-size: 24px; background: #000; 
        color: #00ff88; padding: 20px; border-radius: 12px; line-height: 1.2;
        display: inline-block; text-align: left; white-space: pre;
        min-width: 180px; border: 2px solid #58a6ff;
    }}

    .word-box {{ font-size: 38px; font-weight: 900; letter-spacing: 12px; margin: 15px 0; color: #58a6ff; }}

    /* TECLADO STICKER PROFESIONAL */
    div[data-testid="column"] button {{
        background: {cd} !important;
        border: 3px solid black !important;
        border-radius: 10px !important;
        height: 50px !important;
        {txt_style}
        font-size: 20px !important;
        box-shadow: 4px 4px 0px black;
        transition: 0.1s;
    }}
    div[data-testid="column"] button:active {{ transform: translate(3px, 3px); box-shadow: none; }}
    
    .stButton > button[key="th"] {{ background: #58a6ff !important; color: white !important; -webkit-text-stroke: 0px !important; box-shadow: none; border:none!important; }}
</style>""", unsafe_allow_html=True)

# 3. ETAPAS DEL MUÑECO (CARACTERES ESTÁNDAR PARA EVITAR BUGS)
stages = {
    6: "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    5: "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    4: "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    3: "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    2: "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    1: "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    0: "  +---+\n  |   |\n  X   |\n /|\\  |\n / \\  |\n      |\n========="
}

# 4. INTERFAZ
c1, c2 = st.columns([0.85, 0.15])
c1.markdown("### 🕹️ AHORCADO ONLINE")
if c2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    pi = st.text_input("🔑 ELIGE UNA PALABRA:", type="password")
    if st.button("🚀 COMENZAR PARTIDA", use_container_width=True):
        if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if won: st.balloons(); st.markdown("### 🏆 ¡GANASTE!")
        else: st.markdown(f"### 💀 GAME OVER<br>LA PALABRA ERA: **{s['p'].upper()}**", unsafe_allow_html=True)
        if st.button("🔄 NUEVA PARTIDA", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Layout 100% Vertical
        st.markdown(f"""<div class='v-stack'>
            <div class='card'>
                <pre class='hangman-box'>{stages[s['v']]}</pre>
                <div style='margin-top:10px; font-weight:bold;'>VIDAS: {s['v']} / 6</div>
                <div class='word-box'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        # Teclado Sticker
        cols = st.columns
