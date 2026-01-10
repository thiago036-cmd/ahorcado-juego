import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. UI MODERNA Y VERTICAL
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
color_muñeco = "#ff4b4b" if s["v"] <= 1 else "#00ff88"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; }}
    .card {{ background:{cd}; border:1px solid {br}; border-radius:16px; padding:20px; width: 100%; box-shadow: 0 4px 10px rgba(0,0,0,0.3); }}
    /* FIX PARA EL MUÑECO: Fuente monoespaciada pura y sin saltos raros */
    .hangman {{ 
        font-family: 'Courier New', Courier, monospace !important; 
        font-size: 22px !important; 
        background: #000; 
        color: {color_muñeco}; 
        padding: 20px; 
        border-radius: 12px; 
        line-height: 1.2 !important; 
        display: inline-block; 
        text-align: left;
        white-space: pre !important;
    }}
    .word-box {{ font-size: 35px; font-weight: 800; letter-spacing: 10px; margin: 20px 0; color: #58a6ff; }}
    div[data-testid="column"] button {{ background:{cd}!important; color:{tx}!important; border:1px solid {br}!important; height:45px!important; }}
</style>""", unsafe_allow_html=True)

# 3. ETAPAS DEL MUÑECO CORREGIDAS
stages = {
    6: "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    5: "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    4: "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    3: "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    2: "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    1: "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    0: "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n========="
}

# 4. INTERFAZ PRINCIPAL
c1, c2 = st.columns([0.85, 0.15])
c1.markdown("## 🕹️ AHORCADO ONLINE")
if c2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    pi = st.text_input("🔑 Palabra secreta:", type="password", placeholder="Escribe aquí...")
    if st.button("🚀 EMPEZAR JUEGO", use_container_width=True):
        if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if won: st.balloons(); st.markdown("### 🏆 ¡VICTORIA!")
        else: st.markdown(f"### 💀 FIN DEL JUEGO<br>La palabra era: **{s['p'].upper()}**", unsafe_allow_html=True)
        if st.button("🔄 REINTENTAR", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Visualización Vertical Centrada
        st.markdown(f"""<div class='v-stack'>
            <div class='card'>
                <pre class='hangman'>{stages[s['v']]}</pre>
                <div style='margin-top:15px; font-weight:bold; font-size:20px;'>❤️ VIDAS: {s['v']} / 6</div>
                <div class='word-box'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        # Teclado con Emojis
        st.write("---")
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                l_low = l.lower()
                if l_low in s["u"]:
                    icon = "🟢" if l_low in s["p"] else "❌"
                    st.markdown(f"<div style='text-align:center; font-size:12px;'>{icon}<br><b>{l}</b></div>", unsafe_allow_html=True)
                elif st.button(l, key=f"k-{l}"):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        # Arriesgar
        st.write("")
        if st.button("🔥 ARRIESGAR TODO", use_container_width=True): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("🎯 ¿Cuál es la palabra?:", key="guess").lower().strip()
            if st.button("✔️ ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
