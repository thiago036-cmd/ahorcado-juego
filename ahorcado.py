import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO GLOBAL Y CONFIGURACIÓN
st.set_page_config(page_title="Ahorcado Pro", layout="centered")

@st.cache_resource
def get_state():
    return {"word": "", "used": [], "lives": 6, "win": False, "betting": False}

s = get_state()
st_autorefresh(interval=2000, key="refresh")

# 2. CSS PARA INTERFAZ BONITA Y TECLADO ESTABLE
color_ui = "#00ff88" if s["lives"] >= 4 else "#ffcc00" if s["lives"] >= 2 else "#ff4444"

st.markdown(f"""
    <style>
    .stApp {{ background-color: #0f172a; color: white; }}
    
    /* DISEÑO DEL MUÑECO */
    .m-box {{
        background: #1e293b; border: 3px solid {color_ui}; border-radius: 20px;
        padding: 15px; width: 140px; margin: 0 auto 10px auto;
        text-align: center; box-shadow: 0 0 20px {color_ui}44;
    }}
    .m-text {{
        font-family: 'Courier New', monospace; font-size: 18px; color: {color_ui};
        white-space: pre; line-height: 1.1; display: inline-block; text-align: left;
    }}

    /* PALABRA SELECCIONADA */
    .word-display {{
        font-size: 10vw; font-weight: 900; color: #fbbf24;
        text-align: center; margin: 20px 0; letter-spacing: 5px;
        text-shadow: 2px 2px #000;
    }}

    /* EL TECLADO (SOLUCIÓN DEFINITIVA) */
    .keyboard-container {{
        display: grid;
        grid-template-columns: repeat(7, 1fr);
        gap: 8px;
        max-width: 400px;
        margin: 0 auto;
    }}
    
    .letter-btn {{
        background: #1e293b; border: 2px solid #475569; border-radius: 8px;
        color: white; padding: 10px 0; text-align: center;
        font-weight: bold; font-size: 18px; cursor: pointer;
    }}

    /* BOTÓN ARRIESGAR */
    .btn-orange {{
        background: linear-gradient(135deg, #f59e0b, #d97706);
        border: 2px solid white; border-radius: 10px;
        color: white; font-weight: bold; padding: 10px 20px;
        text-align: center; float: right; cursor: pointer;
        text-decoration: none; display: inline-block;
    }}
    </style>
    """, unsafe_allow_html=True)

# 3. FUNCIONES
def get_drawing(i):
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

# 4. FLUJO DE PANTALLAS
if not s["word"]:
    st.title("🎯 Ahorcado Co-op")
    w = st.text_input("Escribe la palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR JUEGO", use_container_width=True):
        if w: s["word"] = w.lower().strip(); st.rerun()
else:
    won = all(l in s["used"] or l == " " for l in s["word"]) or s["win"]
    if won or s["lives"] <= 0:
        if won: st.success(f"🏆 ¡VICTORIA! ERA: {s['word'].upper()}")
        else: st.error(f"💀 DERROTA. ERA: {s['word'].upper()}")
        if st.button("🔄 JUGAR DE NUEVO", use_container_width=True):
            s.update({"word": "", "used": [], "lives": 6, "win": False, "betting": False})
            st.rerun()
    else:
        # A. Muñeco y Vidas
        st.markdown(f'<div class="m-box"><div class="m-text">{get_drawing(s["lives"])}</div></div>', unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'>❤️ Vidas: <b>{s['lives']}</b></div>", unsafe_allow_html=True)

        # B. Palabra
        v_word = " ".join([l.upper() if l in s["used"] or l == " " else "_" for l in s["word"]])
        st.markdown(f'<div class="word-display">{v_word}</div>', unsafe_allow_html=True)

        # C. Teclado (Usando botones nativos de Streamlit pero con lógica robusta)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7) # En celular, esto ahora se respeta mejor con el CSS anterior
        for i, letra in enumerate(abc):
            l = letra.lower()
            with cols[i % 7]:
                if l in s["used"]:
                    color_status = "#00ff88" if l in s["word"] else "#ff4444"
                    st.markdown(f"<div style='text-align:center; color:{color_status}; font-weight:bold; height:45px; line-height:45px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"k-{letra}"):
                        s["used"].append(l)
                        if l not in s["word"]: s["lives"] -= 1
                        st.rerun()

        # D. Arriesgar abajo derecha
        st.write("---")
        c1, c2 = st.columns([0.6, 0.4])
        with c2:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["betting"] = not s["betting"]
                st.rerun()

        if s["betting"]:
            guess = st.text_input("Escribe la palabra:", key="guess").lower().strip()
            if st.button("✔️ ENVIAR"):
                if guess == s["word"]: s["win"] = True
                else: s["lives"] = 0
                st.rerun()
