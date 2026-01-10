import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO UI (TECLADO STICKER Y CONTENEDORES)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
sticker_txt = "color: white !important; -webkit-text-stroke: 1.5px black !important; font-weight: 900 !important;" if not s["dark"] else f"color: {tx} !important; font-weight: 700 !important;"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: 'Segoe UI', sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .card {{ background:{cd}; border:2px solid {br}; border-radius:24px; padding:30px; width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.3); margin-bottom: 20px; }}
    .word-box {{ font-size: 40px; font-weight: 900; letter-spacing: 12px; margin: 20px 0; color: #58a6ff; text-transform: uppercase; }}
    
    /* TECLADO STICKER */
    div[data-testid="column"] button {{
        background: {cd} !important;
        border: 3px solid black !important;
        border-radius: 12px !important;
        height: 55px !important;
        {sticker_txt}
        font-size: 22px !important;
        box-shadow: 4px 4px 0px black;
    }}
</style>""", unsafe_allow_html=True)

# 3. FUNCIÓN DE DIBUJO SVG (MUÑECO REAL)
def draw_hangman(v):
    color = "#7cfc00" if v > 1 else "#ff4b4b" # Verde neón, rojo en la última vida
    struct = "#ffffff" # Estructura de la horca blanca
    
    # Partes del cuerpo según vidas
    head = f'<circle cx="140" cy="70" r="15" stroke="{color}" stroke-width="4" fill="none" />' if v <= 5 else ""
    body = f'<line x1="140" y1="85" x2="140" y2="140" stroke="{color}" stroke-width="4" />' if v <= 4 else ""
    arm1 = f'<line x1="140" y1="100" x2="110" y2="120" stroke="{color}" stroke-width="4" />' if v <= 3 else ""
    arm2 = f'<line x1="140" y1="100" x2="170" y2="120" stroke="{color}" stroke-width="4" />' if v <= 2 else ""
    leg1 = f'<line x1="140" y1="140" x2="115" y2="175" stroke="{color}" stroke-width="4" />' if v <= 1 else ""
    leg2 = f'<line x1="140" y1="140" x2="165" y2="175" stroke="{color}" stroke-width="4" />' if v <= 0 else ""
    
    # Cara de derrota
    if v == 0:
        head = f'''
        <circle cx="140" cy="70" r="15" stroke="{color}" stroke-width="4" fill="none" />
        <line x1="135" y1="65" x2="145" y2="75" stroke="{color}" stroke-width="2" />
        <line x1="145" y1="65" x2="135" y2="75" stroke="{color}" stroke-width="2" />
        '''

    svg_code = f"""
    <svg width="200" height="200" viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg">
        <line x1="20" y1="190" x2="100" y2="190" stroke="{struct}" stroke-width="6" />
        <line x1="60" y1="190" x2="60" y2="20" stroke="{struct}" stroke-width="6" />
        <line x1="60" y1="20" x2="140" y2="20" stroke="{struct}" stroke-width="6" />
        <line x1="60" y1="50" x2="90" y2="20" stroke="{struct}" stroke-width="4" />
        <line x1="140" y1="20" x2="140" y2="55" stroke="{struct}" stroke-width="2" />
        {head} {body} {arm1} {arm2} {leg1} {leg2}
    </svg>
    """
    st.markdown(f'<div style="display:flex; justify-content:center; background:#000; padding:10px; border-radius:15px; border:2px solid #30363d;">{svg_code}</div>', unsafe_allow_html=True)

# 4. FLUJO DE LA INTERFAZ
c1, c2 = st.columns([0.85, 0.15])
c1.markdown("## 🕹️ AHORCADO ONLINE")
if c2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    pi = st.text_input("🔑 ELIGE LA PALABRA:", type="password")
    if st.button("🚀 EMPEZAR JUEGO", use_container_width=True):
        if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if won: st.balloons(); st.markdown("### 🏆 ¡LO LOGRASTE!")
        else: st.markdown(f"### 💀 FIN DEL JUEGO<br>ERA: **{s['p'].upper()}**", unsafe_allow_html=True)
        if st.button("🔄 VOLVER A JUGAR", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("<div class='card v-stack'>", unsafe_allow_html=True)
        draw_hangman(s["v"])
        st.markdown(f"<div style='margin-top:15px; font-weight:bold; font-size:22px;'>VIDAS: {s['v']} / 6</div>", unsafe_allow_html=True)
        st.markdown(f"<div class='word-box'>{' '.join([l if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>", unsafe_allow_html=True)
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Teclado Sticker
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                l_low = l.lower()
                if l_low in s["u"]:
                    icon = "✅" if l_low in s["p"] else "❌"
                    st.markdown(f"<div style='text-align:center;'>{icon}<br><b>{l}</b></div>", unsafe_allow_html=True)
                elif st.button(l, key=f"btn-{l}"):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        st.write("")
        if st.button("🔥 ARRIESGAR TODO", use_container_width=True): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("🎯 ¿CUÁL ES LA PALABRA?", key="guess").lower().strip()
            if st.button("✔️ ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
