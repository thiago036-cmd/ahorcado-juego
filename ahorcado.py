import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO UI (TECLADO STICKER Y CONTENEDORES MÓVILES)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
sticker_txt = "color: white !important; -webkit-text-stroke: 1.5px black !important; font-weight: 900 !important;" if not s["dark"] else f"color: {tx} !important; font-weight: 700 !important;"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .card {{ background:{cd}; border:2px solid {br}; border-radius:20px; padding:15px; width: 100%; margin-bottom: 10px; }}
    .word-box {{ font-size: 32px; font-weight: 900; letter-spacing: 8px; margin: 15px 0; color: #58a6ff; text-transform: uppercase; }}
    
    /* FIX PARA CELULAR: Contenedor de ancho fijo para el SVG */
    .svg-container {{
        background: #11151c;
        border: 2px solid #7cfc00;
        border-radius: 15px;
        width: 220px;
        height: 220px;
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 0 auto;
    }}

    /* TECLADO STICKER MÓVIL */
    div[data-testid="column"] button {{
        background: {cd} !important;
        border: 2px solid black !important;
        border-radius: 8px !important;
        height: 45px !important;
        width: 100% !important;
        {sticker_txt}
        font-size: 18px !important;
        box-shadow: 2px 2px 0px black;
        margin-bottom: 5px;
    }}
</style>""", unsafe_allow_html=True)

# 3. DIBUJO SVG (REDISEÑADO PARA SER IDÉNTICO A TU IMAGEN VERDE)
def draw_hangman(v):
    color = "#7cfc00" # El verde neón de tu imagen
    
    # Partes del personaje
    head = f'<circle cx="140" cy="70" r="15" stroke="{color}" stroke-width="3" fill="none" />' if v <= 5 else ""
    body = f'<line x1="140" y1="85" x2="140" y2="135" stroke="{color}" stroke-width="3" />' if v <= 4 else ""
    arm1 = f'<line x1="140" y1="100" x2="115" y2="120" stroke="{color}" stroke-width="3" />' if v <= 3 else ""
    arm2 = f'<line x1="140" y1="100" x2="165" y2="120" stroke="{color}" stroke-width="3" />' if v <= 2 else ""
    leg1 = f'<line x1="140" y1="135" x2="115" y2="165" stroke="{color}" stroke-width="3" />' if v <= 1 else ""
    leg2 = f'<line x1="140" y1="135" x2="165" y2="165" stroke="{color}" stroke-width="3" />' if v <= 0 else ""

    svg_code = f"""
    <svg width="180" height="180" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <line x1="40" y1="180" x2="100" y2="180" stroke="{color}" stroke-width="5" />
        <line x1="70" y1="180" x2="70" y2="20" stroke="{color}" stroke-width="5" />
        <line x1="70" y1="20" x2="140" y2="20" stroke="{color}" stroke-width="5" />
        <line x1="70" y1="50" x2="100" y2="20" stroke="{color}" stroke-width="3" />
        <line x1="140" y1="20" x2="140" y2="55" stroke="{color}" stroke-width="2" />
        {head} {body} {arm1} {arm2} {leg1} {leg2}
    </svg>
    """
    st.markdown(f'<div class="svg-container">{svg_code}</div>', unsafe_allow_html=True)

# 4. INTERFAZ
c1, c2 = st.columns([0.8, 0.2])
c1.markdown("### 🕹️ AHORCADO")
if c2.button("🌓"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    pi = st.text_input("🔑 PALABRA:", type="password")
    if st.button("🚀 EMPEZAR", use_container_width=True):
        if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if won: st.success("🏆 ¡GANASTE!"); st.balloons()
        else: st.error(f"💀 PERDISTE: {s['p'].upper()}")
        if st.button("🔄 REINTENTAR", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Área del Muñeco
        draw_hangman(s["v"])
        st.markdown(f"<div class='v-stack'><div class='word-box'>{' '.join([l if l in s['u'] or l==' ' else '_' for l in s['p']])}</div></div>", unsafe_allow_html=True)
        st.write(f"❤️ **Vidas:** {s['v']}/6")
        
        # Teclado (Adaptado para móvil: 6 columnas)
        cols = st.columns(6)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%6]:
                l_low = l.lower()
                if l_low in s["u"]:
                    st.button(l, key=f"b-{l}", disabled=True)
                elif st.button(l, key=f"b-{l}"):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
