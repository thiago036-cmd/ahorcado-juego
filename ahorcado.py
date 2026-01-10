import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Ahorcado Online", layout="centered")

@st.cache_resource
def engine():
    return {
        "p": "", "u": [], "v": 6, "win": False, "bet": False,
        "dark_mode": True 
    }

s = engine()
st_autorefresh(interval=2500, key="global_sync")

# --- 2. COLORES (BÁSICO Y BONITO) ---
if s["dark_mode"]:
    bg, card, txt, border = "#0e1117", "#161b22", "#ffffff", "#30363d"
    btn_key, btn_hover = "#21262d", "#30363d"
else:
    bg, card, txt, border = "#ffffff", "#f6f8fa", "#1f2328", "#d0d7de"
    btn_key, btn_hover = "#ffffff", "#f3f4f6"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Segoe+UI:wght@400;600;700&display=swap');
    
    .stApp {{ background-color: {bg}; color: {txt}; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }}
    
    /* CABECERA */
    .title {{ text-align: center; font-weight: 700; font-size: 2rem; margin-bottom: 20px; color: #58a6ff; }}

    /* TARJETA DE JUEGO */
    .game-card {{
        background: {card}; border-radius: 12px; padding: 25px;
        border: 1px solid {border}; margin-bottom: 20px;
        text-align: center;
    }}

    /* EL MUÑECO (FIJO Y CLARO) */
    .hangman-box {{
        font-family: monospace; font-size: 18px; line-height: 1.2;
        background: #000; color: #39ff14; padding: 15px;
        border-radius: 8px; display: inline-block; margin-bottom: 15px;
    }}

    /* PALABRA */
    .word-display {{ font-size: 32px; font-weight: 700; letter-spacing: 10px; margin: 20px 0; }}

    /* TECLADO */
    .keyboard-container {{
        background: {card}; border: 1px solid {border}; padding: 15px; border-radius: 12px;
    }}
    
    div[data-testid="column"] button {{
        background: {btn_key} !important; border: 1px solid {border} !important;
        color: {txt} !important; border-radius: 6px !important;
        height: 45px !important; font-weight: 600 !important;
    }}
    
    div[data-testid="column"] button:hover {{ background: {btn_hover} !important; }}

    /* BOTONES ESPECIALES */
    .stButton > button[key="toggle_theme"] {{ background: #58a6ff !important; color: white !important; border: none !important; }}
    .stButton > button[key*="btn-arr"] {{ background: #f78166 !important; color: white !important; border: none !important; }}

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

# --- 3. INTERFAZ PRINCIPAL ---
cols_top = st.columns([0.8, 0.2])
with cols_top[0]:
    st.markdown("<div class='title'>AHORCADO ONLINE</div>", unsafe_allow_html=True)
with cols_top[1]:
    if st.button("🌓", key="toggle_theme"):
        s["dark_mode"] = not s["dark_mode"]
        st.rerun()

if not s["p"]:
    with st.container():
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        p_input = st.text_input("Ingresa la palabra para jugar:", type="password")
        if st.button("COMENZAR PARTIDA", use_container_width=True):
            if p_input:
                s.update({"p": p_input.lower().strip(), "u": [], "v": 6, "win": False})
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    win = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    
    if win or s["v"] <= 0:
        st.markdown("<div class='game-card'>", unsafe_allow_html=True)
        if win:
            st.balloons()
            st.success("¡FELICIDADES, GANASTE!")
        else:
            st.error(f"GAME OVER. La palabra era: {s['p'].upper()}")
        
        if st.button("NUEVA PARTIDA", use_container_width=True):
            s.update({"p": "", "u": [], "v": 6, "win": False, "bet": False})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Área de Juego
        st.markdown(f"""
            <div class='game-card'>
                <div class='hangman-box'>{get_drawing(s['v'])}</div>
                <div style='font-weight:bold; margin-top:10px;'>Vidas: {s['v']} / 6</div>
                <div class='word-display'>
                    {" ".join([l.upper() if l in s["u"] or l == " " else "_" for l in s["p"]])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Teclado
        st.markdown("<div class='keyboard-container'>", unsafe_allow_html=True)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["u"]:
                    color_l = "#238636" if l_min in s["p"] else "#8b949e"
                    st.markdown(f"<div style='text-align:center; color:{color_l}; font-weight:bold; height:45px; line-height:45px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"btn-{letra}"):
                        s["u"].append(l_min)
                        if l_min not in s["p"]: s["v"] -= 1
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Arriesgar
        st.write("")
        c1, c2 = st.columns([0.7, 0.3])
        with c2:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["bet"] = not s["bet"]
                st.rerun()

        if s["bet"]:
            ans = st.text_input("Escribe la palabra completa:", key="ans").lower().strip()
            if st.button("ENVIAR", use_container_width=True):
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()

# Botón oculto para actualizar por si acaso
if st.button("🔄 Actualizar", key="force_refresh"):
    st.rerun()
