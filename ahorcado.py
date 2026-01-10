import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as cp

st.set_page_config(page_title="Ahorcado", layout="centered")
if "p" not in st.session_state: st.session_state.update({"p":"","u":[],"v":6})
st_autorefresh(interval=2000, key="sync")

st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    [data-testid="stHorizontalBlock"] { display: grid !important; grid-template-columns: repeat(7, 1fr); gap: 5px; }
    button { background:#161b22 !important; border:2px solid #000 !important; border-radius:8px !important; height:45px !important; box-shadow:2px 2px 0 black !important; }
    button p { color:white !important; -webkit-text-stroke:1px black; font-weight:900; font-size:18px; }
    .word { font-size:35px; font-weight:900; letter-spacing:8px; text-align:center; color:#58a6ff; margin:15px 0; }
</style>""", unsafe_allow_html=True)

def draw(v):
    c = "#7cfc00"
    part = lambda cond, draw: draw if cond else ""
    svg = f"""<div style="display:flex;justify-content:center;background:#11151c;border-radius:15px;border:2px solid #30363d;height:160px;">
    <svg width="150" height="150" viewBox="0 0 200 200">
        <path d="M20 190 H100 M60 190 V20 H140 V55" stroke="white" stroke-width="6" fill="none"/>
        {part(v<=5, f'<circle cx="140" cy="70" r="15" stroke="{c}" stroke-width="4" fill="none"/>')}
        {part(v<=4, f'<line x1="140" y1="85" x2="140" y2="140" stroke="{c}" stroke-width="4"/>')}
        {part(v<=3, f'<line x1="140" y1="100" x2="110" y2="120" stroke="{c}" stroke-width="4"/>')}
        {part(v<=2, f'<line x1="140" y1="100" x2="170" y2="120" stroke="{c}" stroke-width="4"/>')}
        {part(v<=1, f'<line x1="140" y1="140" x2="115" y2="175" stroke="{c}" stroke-width="4"/>')}
        {part(v<=0, f'<line x1="140" y1="140" x2="165" y2="175" stroke="{c}" stroke-width="4"/>')}
    </svg></div>"""
    cp.html(svg, height=170)

st.title("🕹️ AHORCADO")
s = st.session_state
if not s.p:
    p = st.text_input("PALABRA:", type="password")
    if st.button("JUGAR"): s.p, s.u, s.v = p.lower().strip(), [], 6; st.rerun()
else:
    win = all(l in s.u or l==" " for l in s.p)
    if win or s.v <= 0:
        st.write("🏆 GANASTE" if win else f"💀 PERDISTE: {s.p.upper()}")
        if st.button("OTRA"): s.p = ""; st.rerun()
    else:
        draw(s.v)
        st.markdown(f"<div class='word'>{' '.join([l.upper() if l in s.u or l==' ' else '_' for l in s.p])}</div>", unsafe_allow_html=True)
        st.write(f"❤️ Vidas: {s.v}/6")
        cols = st.columns(27)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i]:
                if l.lower() in s.u: st.button("✅" if l.lower() in s.p else "❌", key=l, disabled=True)
                elif st.button(l, key=l):
                    s.u.append(l.lower())
                    if l.lower() not in s.p: s.v -= 1
                    st.rerun()
