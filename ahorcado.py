import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as components

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO UI
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
sticker_txt = "color: white !important; -webkit-text-stroke: 1.5px black !important; font-weight: 900 !important;" if not s["dark"] else f"color: {tx} !important; font-weight: 700 !important;"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; width: 100%; }}
    .card {{ background:{cd}; border:2px solid {br}; border-radius:20px; padding:15px; width: 100%; margin-bottom: 10px; }}
    .word-box {{ font-size: 32px; font-weight: 900; letter-spacing: 8px; margin: 15px 0; color: #58a6ff; text-transform: uppercase; text-align: center; }}
    
    div[data-testid="column"] button {{
        background: {cd} !important;
        border: 2px solid black !important;
        border-radius: 8px !important;
        height: 50px !important;
        width: 100% !important;
        {sticker_txt}
        font-size: 20px !important;
        box-shadow: 3px 3px 0px black;
    }}
</style>""", unsafe_allow_html=True)

# 3. DIBUJO "BLINDADO" (ST.COMPONENTS PARA MÓVIL)
def draw_hangman_safe(v):
    color = "#7cfc00"
    head = f'<circle cx="140" cy="70" r="15" stroke="{color}" stroke-width="4" fill="none" />' if v <= 5 else ""
    body = f'<line x1="140" y1="85" x2="140" y2="140" stroke="{color}" stroke-width="4" />' if v <= 4 else ""
    arm1 = f'<line x1="140" y1="100" x2="110" y2="120" stroke="{color}" stroke-width="4" />' if v <= 3 else ""
    arm2 = f'<line x1="140" y1="100" x2="170" y2="120" stroke="{color}" stroke-width="4" />' if v <= 2 else ""
    leg1 = f'<line x1="140" y1="140" x2="115" y2="175" stroke="{color}" stroke-width="4" />' if v <= 1 else ""
    leg2 = f'<line x1="140" y1="140" x2="165" y2="175" stroke="{color}" stroke-width="4" />' if v <= 0 else ""

    # HTML puro para el iframe
    html_content = f"""
    <div style="display: flex; justify-content: center; align-items: center; background: #11151c; border-radius: 15px; border: 2px solid #7cfc00; height: 190px;">
        <svg width="180" height="180" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
            <line x1="20" y1="190" x2="100" y2="190" stroke="{color}" stroke-width="6" />
            <line x1="60" y1="190" x2="60" y2="20" stroke="{color}" stroke-width="6" />
            <line x1="60" y1="20" x2="140" y2="20" stroke="{color}" stroke-width="6" />
            <line x1="60" y1="50" x2="90" y2="20" stroke="{color}" stroke-width="4" />
            <line x1="140" y1="20" x2="140" y2="55" stroke="{color}" stroke-width="2" />
            {head} {body} {arm1} {arm2} {leg1} {leg2}
        </svg>
    </div>
    """
    # Forzamos el renderizado como HTML real
    components.html(html_content, height=200)

# 4. INTERFAZ
col_t1, col_t2 = st.columns([0.8, 0.2])
col_t1.markdown("### 🕹️ AHORCADO")
if col_t2.button("🌓"): s["dark"] = not s["dark"]; st.rerun()

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
        # Dibujo
        draw_hangman_safe(s["v"])
        
        # Palabra y Vidas
        st.markdown(f"<div class='word-box'>{' '.join([l if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>", unsafe_allow_html=True)
        st.write(f"❤️ **Vidas:** {s['v']}/6")
        
        # Teclado (Adaptado a 6 columnas para dedos grandes en móvil)
        cols = st.columns(6)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%6]:
                l_low = l.lower()
                if l_low in s["u"]:
                    st.button(l, key=f"k-{l}", disabled=True)
                elif st.button(l, key=f"k-{l}"):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
