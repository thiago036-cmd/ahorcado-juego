import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# 1. CONFIGURACIÓN Y ESTADO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
if "p" not in st.session_state:
    st.session_state.update({"p": "", "u": [], "v": 6, "win": False})

st_autorefresh(interval=2000, key="sync")

# 2. CSS PARA ARREGLAR LAS LETRAS Y EL DISEÑO
st.markdown(f"""<style>
    .stApp {{ background-color: #0e1117; color: white; }}
    
    /* TÍTULO Y CONTENEDORES */
    .main-title {{ text-align: center; color: white; font-weight: 800; margin-bottom: 20px; }}
    .word-box {{ 
        font-size: 40px; font-weight: 900; letter-spacing: 10px; 
        text-align: center; color: #58a6ff; margin: 20px 0; 
    }}

    /* EL TECLADO: ARREGLO DE COLOR Y ALINEACIÓN */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 8px !important;
    }}
    
    [data-testid="column"] {{
        flex: 0 1 auto !important;
        min-width: 45px !important;
    }}

    /* BOTONES ESTILO STICKER (LETRAS BLANCAS FORZADAS) */
    button {{
        background-color: #161b22 !important;
        border: 2px solid black !important;
        border-radius: 10px !important;
        height: 50px !important;
        width: 45px !important;
        color: white !important; /* Letras blancas */
        -webkit-text-stroke: 1px black !important; /* Borde de la letra */
        font-weight: 900 !important;
        font-size: 20px !important;
        box-shadow: 3px 3px 0px black !important;
    }}
    
    /* Botones cuando ya se usaron */
    button:disabled {{
        background-color: #0d1117 !important;
        border-color: #30363d !important;
        color: #555 !important;
        -webkit-text-stroke: 0px !important;
        box-shadow: none !important;
    }}
</style>""", unsafe_allow_html=True)

# 3. DIBUJO DEL MUÑECO (RESTAURADO Y FIJO)
def draw_hangman(v):
    color = "#7cfc00"
    head = f'<circle cx="140" cy="70" r="15" stroke="{color}" stroke-width="4" fill="none" />' if v <= 5 else ""
    body = f'<line x1="140" y1="85" x2="140" y2="140" stroke="{color}" stroke-width="4" />' if v <= 4 else ""
    arm1 = f'<line x1="140" y1="100" x2="110" y2="120" stroke="{color}" stroke-width="4" />' if v <= 3 else ""
    arm2 = f'<line x1="140" y1="100" x2="170" y2="120" stroke="{color}" stroke-width="4" />' if v <= 2 else ""
    leg1 = f'<line x1="140" y1="140" x2="115" y2="175" stroke="{color}" stroke-width="4" />' if v <= 1 else ""
    leg2 = f'<line x1="140" y1="140" x2="165" y2="175" stroke="{color}" stroke-width="4" />' if v <= 0 else ""

    html = f"""
    <div style="display: flex; justify-content: center; background: #000; padding: 10px; border-radius: 15px; border: 2px solid #30363d;">
        <svg width="180" height="180" viewBox="0 0 200 200">
            <line x1="20" y1="190" x2="100" y2="190" stroke="white" stroke-width="6" />
            <line x1="60" y1="190" x2="60" y2="20" stroke="white" stroke-width="6" />
            <line x1="60" y1="20" x2="140" y2="20" stroke="white" stroke-width="6" />
            <line x1="140" y1="20" x2="140" y2="55" stroke="white" stroke-width="2" />
            {head} {body} {arm1} {arm2} {leg1} {leg2}
        </svg>
    </div>
    """
    components.html(html, height=200)

# 4. LÓGICA DE INTERFAZ
st.markdown("<h1 class='main-title'>🕹️ AHORCADO ONLINE</h1>", unsafe_allow_html=True)

if not st.session_state.p:
    pi = st.text_input("🔑 PALABRA SECRETA:", type="password")
    if st.button("🚀 EMPEZAR", use_container_width=True):
        if pi:
            st.session_state.p = pi.lower().strip()
            st.session_state.u = []
            st.session_state.v = 6
            st.rerun()
else:
    won = all(l in st.session_state.u or l == " " for l in st.session_state.p)
    
    if won or st.session_state.v <= 0:
        if won: st.success("🏆 ¡GANASTE!"); st.balloons()
        else: st.error(f"💀 PERDISTE. ERA: {st.session_state.p.upper()}")
        if st.button("🔄 NUEVA PARTIDA", use_container_width=True):
            st.session_state.p = ""
            st.rerun()
    else:
        # Mostrar Muñeco
        draw_hangman(st.session_state.v)
        
        # Mostrar Palabra
        display_word = " ".join([l.upper() if l in st.session_state.u or l == " " else "_" for l in st.session_state.p])
        st.markdown(f"<div class='word-box'>{display_word}</div>", unsafe_allow_html=True)
        st.write(f"❤️ Vidas: {st.session_state.v}/6")
        
        # Teclado Sticker (Letras Blancas con Borde Negro)
        alphabet = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(alphabet))
        for i, l in enumerate(alphabet):
            with cols[i]:
                l_low = l.lower()
                if l_low in st.session_state.u:
                    st.button(l, key=f"k-{l}", disabled=True)
                else:
                    if st.button(l, key=f"k-{l}"):
                        st.session_state.u.append(l_low)
                        if l_low not in st.session_state.p:
                            st.session_state.v -= 1
                        st.rerun()
