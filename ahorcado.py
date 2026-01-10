import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO UI (EL TECLADO QUE TE GUSTA Y EL MUÑECO CORREGIDO)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
sticker_txt = "color: white !important; -webkit-text-stroke: 1.5px black !important; font-weight: 900 !important;" if not s["dark"] else f"color: {tx} !important; font-weight: 700 !important;"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: 'Segoe UI', sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .card {{ background:{cd}; border:2px solid {br}; border-radius:24px; padding:30px; width: 100%; box-shadow: 0 10px 30px rgba(0,0,0,0.3); }}

    .word-box {{ font-size: 40px; font-weight: 900; letter-spacing: 12px; margin: 20px 0; color: #58a6ff; }}

    /* TECLADO STICKER (COMO PEDISTE) */
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

# 3. ETAPAS DEL MUÑECO (ESTILO LINEAL DE TU IMAGEN)
# He usado caracteres de líneas finas para que no parezcan bloques
stages = {
    6: "🏗️\n\n\n",
    5: "🏗️\n  😶\n\n",
    4: "🏗️\n  😶\n  👕\n",
    3: "🏗️\n  😶\n /👕\n",
    2: "🏗️\n  😶\n /👕\\\n",
    1: "🏗️\n  😶\n /👕\\\n /",
    0: "🏗️\n  💀\n /👕\\\n / \\"
}

# 4. INTERFAZ
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
        st.markdown(f"""<div class='v-stack'>
            <div class='card'>
                <pre class='hangman-box'>{stages[s['v']]}</pre>
                <div style='margin-top:15px; font-weight:bold; font-size:22px;'>VIDAS: {s['v']} / 6</div>
                <div class='word-box'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        st.write("---")
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

        if st.button("🔥 ARRIESGAR TODO", use_container_width=True): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("🎯 ESCRIBE LA PALABRA:", key="guess").lower().strip()
            if st.button("✔️ ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()

