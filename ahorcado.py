import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as cp

# --- CONFIGURACIÓN PARA SERVIDOR ONLINE ---
st.set_page_config(page_title="Ahorcado Online", layout="centered") 

# Forzamos que la sesión sea global para el navegador actual
if "p" not in st.session_state: 
    st.session_state.update({"p":"","u":[],"v":6})

# Esto mantiene la conexión viva con el servidor cada 2 segundos
st_autorefresh(interval=2000, key="online_sync")

st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    [data-testid="stHorizontalBlock"] { 
        display: grid !important; 
        grid-template-columns: repeat(auto-fit, minmax(60px, 1fr)) !important; 
        gap: 8px !important; justify-content: center !important;
    }
    button { 
        background:#1c2128 !important; border: none !important; border-radius:8px !important; 
        height:55px !important; min-width:60px !important;
        display: flex !important; align-items: center !important; justify-content: center !important; 
    }
    button p { color:white !important; font-weight:800 !important; font-size:20px !important; margin:0 !important; }
    .w { font-size:35px; font-weight:900; letter-spacing:10px; text-align:center; color:#58a6ff; margin:20px 0; font-family:monospace; }
</style>""", unsafe_allow_html=True)

def draw(v):
    c, p = "#7cfc00", lambda cond, d: d if cond else ""
    svg = f"""<div style="display:flex;justify-content:center;background:#11151c;border-radius:15px;height:160px;">
    <svg width="140" height="140" viewBox="0 0 200 200"><path d="M20 180 H100 M60 180 V20 H140 V50" stroke="white" stroke-width="6" fill="none"/>
        {p(v<=5, f'<circle cx="140" cy="65" r="15" stroke="{c}" stroke-width="4" fill="none"/>')}
        {p(v<=4, f'<line x1="140" y1="80" x2="140" y2="130" stroke="{c}" stroke-width="4"/>')}
        {p(v<=3, f'<line x1="140" y1="95" x2="115" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=2, f'<line x1="140" y1="95" x2="165" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=1, f'<line x1="140" y1="130" x2="115" y2="160" stroke="{c}" stroke-width="4"/>')}
        {p(v<=0, f'<line x1="140" y1="130" x2="165" y2="160" stroke="{c}" stroke-width="4"/>')}
    </svg></div>"""
    cp.html(svg, height=170)

st.title("🕹️ AHORCADO")
s = st.session_state

if not s.p:
    txt = st.text_input("Ingresa la palabra secreta:", type="password", key="input_palabra")
    if st.button("🚀 EMPEZAR JUEGO", use_container_width=True):
        if txt: 
            s.p = txt.lower().strip()
            s.u = []
            s.v = 6
            st.rerun()
else:
    win = all(l in s.u or l==" " for l in s.p)
    if win or s.v <= 0:
        st.write("🏆 ¡GANASTE!" if win else f"💀 PALABRA: {s.p.upper()}")
        if st.button("🔄 REINTENTAR", use_container_width=True):
            s.p = ""
            st.rerun()
    else:
        draw(s.v)
        st.markdown(f"<div class='w'>{' '.join([l.upper() if l in s.u or l==' ' else '_' for l in s.p])}</div>", unsafe_allow_html=True)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(abc))
        for i, l in enumerate(abc):
            with cols[i]:
                char = l.lower()
                if char in s.u:
                    st.button("✅" if char in s.p else "❌", key=f"btn_{l}", disabled=True)
                elif st.button(l, key=f"btn_{l}"):
                    s.u.append(char)
                    if char not in s.p: s.v -= 1
                    st.rerun()
