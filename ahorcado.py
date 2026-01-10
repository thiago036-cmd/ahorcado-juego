import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN E INICIO ---
st.set_page_config(page_title="Ahorcado Pro", layout="centered")

@st.cache_resource
def get_state():
    return {"word": "", "used": [], "lives": 6, "win": False, "betting": False}

s = get_state()
st_autorefresh(interval=2000, key="refresh")

# --- 2. CSS ESTILO PREMIUM Y COMPACTO ---
color = "#00ff88" if s["lives"] >= 4 else "#ffcc00" if s["lives"] >= 2 else "#ff4444"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0d1117; color: white; }}
    
    /* Muñeco más pequeño y centrado */
    .m-box {{
        background: #161b22; border: 2px solid {color}; border-radius: 15px;
        padding: 8px; width: 110px; margin: 0 auto; text-align: center;
        box-shadow: 0 0 10px {color}44; font-family: monospace; color: {color};
        white-space: pre; line-height: 1.0; font-size: 13px;
    }}

    /* Palabra con tamaño ajustado para móvil */
    .word-box {{
        font-size: 35px; font-weight: 800; color: #fbbf24;
        text-align: center; margin: 10px 0; letter-spacing: 3px;
    }}

    /* Ajuste de botones para que no se bugueen */
    .stButton > button {{
        width: 100% !important; height: 40px !important;
        padding: 0 !important; font-size: 14px !important;
        border-radius: 6px !important; background: #21262d !important;
        color: white !important; border: 1px solid #30363d !important;
    }}

    /* Botón Arriesgar específico */
    div[data-testid="column"] button[key*="btn-arr"] {{
        background: #e67e22 !important; border: none !important;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- 3. DIBUJO ---
def get_draw(i):
    stages = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=====",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=====",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n====="
    ]
    return stages[i]

# --- 4. LÓGICA DE PANTALLAS ---
if not s["word"]:
    st.title("🏹 Ahorcado Co-op")
    w = st.text_input("Escribe la palabra:", type="password")
    if st.button("🚀 INICIAR"):
        if w: s["word"] = w.lower().strip(); st.rerun()
else:
    won = all(l in s["used"] or l == " " for l in s["word"]) or s["win"]
    if won or s["lives"] <= 0:
        if won: st.success(f"🏆 GANASTE: {s['word'].upper()}")
        else: st.error(f"💀 PERDISTE: {s['word'].upper()}")
        if st.button("🔄 REINICIAR"):
            s.update({"word": "", "used": [], "lives": 6, "win": False, "betting": False})
            st.rerun()
    else:
        # A. Muñeco y Vidas
        st.markdown(f'<div class="m-box">{get_draw(s["lives"])}</div>', unsafe_allow_html=True)
        st.markdown(f"<p style='text-align:center; margin:0;'>❤️ Vidas: {s['lives']}</p>", unsafe_allow_html=True)

        # B. Palabra
        v_word = " ".join([l.upper() if l in s["used"] or l == " " else "_" for l in s["word"]])
        st.markdown(f'<div class="word-box">{v_word}</div>', unsafe_allow_html=True)

        # C. Teclado (7 columnas fijas para móvil)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l = letra.lower()
            with cols[i % 7]:
                if l in s["used"]:
                    c_txt = "#00ff88" if l in s["word"] else "#444"
                    st.markdown(f"<div style='text-align:center; color:{c_txt}; font-size:12px; font-weight:bold;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"k-{letra}"):
                        s["used"].append(l)
                        if l not in s["word"]: s["lives"] -= 1
                        st.rerun()

        # D. Arriesgar (Abajo derecha)
        st.markdown("<br>", unsafe_allow_html=True)
        c1, c2 = st.columns([0.6, 0.4])
        with c2:
            if st.button("🔥 ARRIESGAR", key="btn-arr"):
                s["betting"] = not s["betting"]
                st.rerun()

        if s["betting"]:
            guess = st.text_input("Palabra completa:", key="guess").lower().strip()
            if st.button("✔️ ENVIAR"):
                if guess == s["word"]: s["win"] = True
                else: s["lives"] = 0
                st.rerun()
