import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- 1. CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Ahorcado Pastel Pro", layout="centered")

@st.cache_resource
def engine():
    return {"p": "", "u": [], "v": 6, "win": False, "bet": False}

s = engine()
st_autorefresh(interval=2500, key="global_sync")

# --- 2. DISEÑO UI PASTEL (CLEAN & COMPACT) ---
# Colores dinámicos basados en vidas
color_vida = "#FFB7B2" if s["v"] <= 2 else "#FFDAC1" if s["v"] <= 4 else "#Baffc9"

st.markdown(f"""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Quicksand:wght@500;700&family=JetBrains+Mono&display=swap');
    
    .stApp {{ background-color: #F3F4F6; color: #4B5563; font-family: 'Quicksand', sans-serif; }}
    
    /* TÍTULO */
    .title {{
        text-align: center; font-weight: 700; font-size: 1.8rem;
        color: #6D28D9; margin-bottom: 15px;
    }}

    /* CONTENEDOR PRINCIPAL */
    .game-card {{
        background: white; border-radius: 24px; padding: 20px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.05);
        margin-bottom: 15px; border: 1px solid #E5E7EB;
    }}

    /* ARTE ASCII */
    .ascii-box {{
        font-family: 'JetBrains Mono', monospace; font-size: 12px;
        color: #9CA3AF; line-height: 1.1; display: flex; 
        justify-content: center; margin-bottom: 10px;
    }}

    /* PALABRA */
    .word-display {{
        display: flex; justify-content: center; gap: 8px; margin: 15px 0;
    }}
    .letter-slot {{
        font-size: 24px; font-weight: 700; border-bottom: 3px solid #DDD6FE;
        width: 28px; text-align: center; color: #4C1D95; height: 35px;
    }}

    /* TECLADO CON FONDO UNIDO (PASTEL) */
    .keyboard-bg {{
        background: #F9FAFB; padding: 15px; border-radius: 20px;
        display: grid; grid-template-columns: repeat(7, 1fr); gap: 8px;
        border: 2px solid #F3F4F6;
    }}

    /* BOTONES KEYCAP PASTEL */
    div[data-testid="column"] button {{
        background: #FFFFFF !important; border: 1px solid #E5E7EB !important;
        color: #6B7280 !important; border-radius: 10px !important;
        height: 42px !important; font-weight: 700 !important;
        box-shadow: 0 2px 0 #E5E7EB !important; transition: 0.1s !important;
    }}
    div[data-testid="column"] button:hover {{
        background: #DDD6FE !important; color: #4C1D95 !important;
        border-color: #C4B5FD !important; transform: translateY(2px);
    }}

    /* BOTÓN ARRIESGAR */
    .stButton > button[key*="btn-arr"] {{
        background: #FEF3C7 !important; color: #D97706 !important;
        border: 1px solid #FDE68A !important; border-radius: 12px !important;
        font-size: 13px !important; font-weight: 700 !important;
    }}

    /* STATUS VIDAS */
    .status {{
        text-align: center; font-size: 12px; font-weight: 700;
        color: #9CA3AF; margin-bottom: 5px;
    }}

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
        p_input = st.text_input("Palabra secreta:", type="password")
        if st.form_submit_button("¡EMPEZAR JUEGO!", use_container_width=True):
            if p_input:
                s.update({"p": p_input.lower().strip(), "u": [], "v": 6, "win": False})
                st.rerun()
else:
    win = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    
    if win or s["v"] <= 0:
        st.markdown("<div class='game-card' style='text-align:center;'>", unsafe_allow_html=True)
        if win:
            st.balloons()
            st.markdown("<h2 style='color:#10B981;'>✨ ¡Ganaste! ✨</h2>", unsafe_allow_html=True)
        else:
            st.markdown("<h2 style='color:#EF4444;'>Suerte para la próxima</h2>", unsafe_allow_html=True)
        st.markdown(f"La palabra era: <b style='color:#4C1D95;'>{s['p'].upper()}</b>", unsafe_allow_html=True)
        if st.button("JUGAR OTRA VEZ", use_container_width=True):
            s.update({"p": "", "u": [], "v": 6, "win": False, "bet": False})
            st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='title'>AHORCADO ONLINE</div>", unsafe_allow_html=True)
        
        # Área de dibujo y palabra
        st.markdown(f"""
            <div class='game-card'>
                <div class='ascii-box'>{draw(s['v'])}</div>
                <div class='status'>VIDAS DISPONIBLES: {s['v']} / 6</div>
                <div class='word-display'>
                    {"".join([f"<div class='letter-slot'>{l.upper() if l in s['u'] or l == ' ' else ''}</div>" for l in s['p']])}
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Teclado con fondo unido
        st.markdown("<div class='keyboard-bg'>", unsafe_allow_html=True)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["u"]:
                    # Letras ya usadas
                    color_txt = "#A7F3D0" if l_min in s["p"] else "#F3F4F6"
                    st.markdown(f"<div style='text-align:center; color:{color_txt}; font-weight:700; height:42px; line-height:42px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"btn-{letra}"):
                        s["u"].append(l_min)
                        if l_min not in s["p"]: s["v"] -= 1
                        st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        # Botón Arriesgar compacto
        st.markdown("<div style='display: flex; justify-content: flex-end; margin-top: 15px;'>", unsafe_allow_html=True)
        col1, col2 = st.columns([0.6, 0.4])
        with col2:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["bet"] = not s["bet"]
                st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)

        if s["bet"]:
            ans = st.text_input("Escribe la palabra completa:", key="ans").lower().strip()
            if st.button("ENVIAR RESPUESTA", use_container_width=True):
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
