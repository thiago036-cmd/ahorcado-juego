import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. CONFIGURACIÓN Y ESTADO GLOBAL
st.set_page_config(page_title="Ahorcado Pro", layout="centered")

@st.cache_resource
def get_state():
    return {"word": "", "used": [], "lives": 6, "win": False, "betting": False}

s = get_state()
st_autorefresh(interval=2000, key="refresh") # Sincronización automática

# 2. DISEÑO UI (CSS LIMPIO)
color = "#00ff88" if s["lives"] >= 4 else "#ffcc00" if s["lives"] >= 2 else "#ff4444"

st.markdown(f"""
    <style>
    .stApp {{ background: #0f172a; color: white; }}
    .main {{ padding: 1rem; }}
    
    /* MUÑECO */
    .m-box {{
        background: #1e293b; border: 3px solid {color}; border-radius: 15px;
        padding: 10px; width: 130px; margin: 0 auto; text-align: center;
        box-shadow: 0 0 15px {color}33; font-family: monospace; color: {color};
        white-space: pre; line-height: 1.1; font-size: 15px;
    }}

    /* PALABRA */
    .word {{
        font-size: 10vw; font-weight: 800; color: #fbbf24;
        text-align: center; margin: 15px 0; letter-spacing: 4px;
    }}

    /* TECLADO FLEXIBLE (Solución para Celulares) */
    .keyboard {{
        display: flex; flex-wrap: wrap; justify-content: center; gap: 6px;
        margin: 20px 0;
    }}
    
    .stButton > button {{
        border: 2px solid #475569 !important; border-radius: 10px !important;
        background: #1e293b !important; color: white !important;
        font-weight: bold !important; height: 45px !important; width: 45px !important;
    }}

    /* BOTÓN ARRIESGAR ABAJO DERECHA */
    .area-bottom {{ display: flex; justify-content: flex-end; margin-top: 20px; }}
    .btn-bet button {{
        background: linear-gradient(135deg, #f59e0b, #d97706) !important;
        border: 2px solid white !important; width: 140px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. LÓGICA DE DIBUJO
def draw(i):
    stages = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
    ]
    return stages[i]

# 4. INTERFAZ DE USUARIO
if not s["word"]:
    st.title("🏹 Ahorcado Co-op")
    w = st.text_input("Palabra Secreta:", type="password")
    if st.button("🚀 INICIAR"):
        if w: s["word"] = w.lower().strip(); st.rerun()
else:
    is_win = all(l in s["used"] or l == " " for l in s["word"]) or s["win"]
    if is_win or s["lives"] <= 0:
        if is_win: st.balloons(); st.success(f"GANASTE: {s['word'].upper()}")
        else: st.error(f"PERDISTE: {s['word'].upper()}")
        if st.button("🔄 NUEVA PARTIDA"):
            s.update({"word": "", "used": [], "lives": 6, "win": False, "betting": False})
            st.rerun()
    else:
        # Visualización vertical
        st.markdown(f'<div class="m-box">{draw(s["lives"])}</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; opacity:0.7;'>❤️ Vidas: {s['lives']}</p>", unsafe_allow_html=True)
        
        display_word = " ".join([l.upper() if l in s["used"] or l == " " else "_" for l in s["word"]])
        st.markdown(f'<div class="word">{display_word}</div>', unsafe_allow_html=True)

        # Teclado (Usando columnas de Streamlit pero optimizadas)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l = letra.lower()
            with cols[i % 7]:
                if l in s["used"]:
                    c_txt = "#00ff88" if l in s["word"] else "#ff4444"
                    st.markdown(f"<div style='text-align:center; color:{c_txt}; font-weight:bold; padding:10px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"k-{letra}"):
                        s["used"].append(l)
                        if l not in s["word"]: s["lives"] -= 1
                        st.rerun()

        # Arriesgar abajo derecha
        st.markdown('<div class="area-bottom">', unsafe_allow_html=True)
        col1, col2 = st.columns([0.6, 0.4])
        with col2:
            st.markdown('<div class="btn-bet">', unsafe_allow_html=True)
            if st.button("🔥 ARRIESGAR", key="btn-arr"):
                s["betting"] = not s["betting"]
                st.rerun()
            st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

        if s["betting"]:
            guess = st.text_input("Adivina la palabra:", key="guess").lower().strip()
            if st.button("ENVIAR"):
                if guess == s["word"]: s["win"] = True
                else: s["lives"] = 0
                st.rerun()
