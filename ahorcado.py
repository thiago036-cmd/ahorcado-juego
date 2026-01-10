import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO DEL JUEGO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO DE INTERFAZ (TECLADO PERSONALIZADO)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")

# Estilo específico para las letras en Modo Claro: Blancas con borde negro
txt_style = "color: white; -webkit-text-stroke: 1.5px black; font-weight: 900;" if not s["dark"] else f"color: {tx}; font-weight: 700;"

st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: 'Segoe UI', sans-serif; }}
    .card {{ background:{cd}; border:1px solid {br}; border-radius:20px; padding:25px; text-align:center; box-shadow: 0 8px 16px rgba(0,0,0,0.2); }}
    
    /* DISEÑO DEL MUÑECO REDISEÑADO */
    .hangman-frame {{ 
        font-family: 'Courier New', monospace; font-size: 24px; background: #000; 
        color: #00ffcc; padding: 25px; border-radius: 15px; line-height: 1;
        display: inline-block; text-align: left; white-space: pre;
        border: 2px solid #58a6ff;
    }}

    .word-display {{ font-size: 40px; font-weight: 900; letter-spacing: 12px; margin: 20px 0; color: #58a6ff; }}

    /* TECLADO PERSONALIZADO */
    div[data-testid="column"] button {{
        background: {cd} !important;
        border: 2px solid black !important;
        border-radius: 8px !important;
        height: 50px !important;
        {txt_style}
        font-size: 20px !important;
        transition: 0.1s;
    }}
    div[data-testid="column"] button:hover {{ transform: scale(1.05); border-color: #58a6ff !important; }}

    .stButton > button[key="th"] {{ background: #58a6ff !important; color: white !important; -webkit-text-stroke: 0px !important; }}
</style>""", unsafe_allow_html=True)

# 3. MUÑECO REDISEÑADO POR ETAPAS
stages = {
    6: "  ╔═══╗\n  ║   ║\n      ║\n      ║\n      ║\n      ║\n  ════╩═══",
    5: "  ╔═══╗\n  ║   ║\n  ☺   ║\n      ║\n      ║\n      ║\n  ════╩═══",
    4: "  ╔═══╗\n  ║   ║\n  ☺   ║\n  ║   ║\n      ║\n      ║\n  ════╩═══",
    3: "  ╔═══╗\n  ║   ║\n  ☺   ║\n /║   ║\n      ║\n      ║\n  ════╩═══",
    2: "  ╔═══╗\n  ║   ║\n  ☺   ║\n /║\\  ║\n      ║\n      ║\n  ════╩═══",
    1: "  ╔═══╗\n  ║   ║\n  ☺   ║\n /║\\  ║\n /    ║\n      ║\n  ════╩═══",
    0: "  ╔═══╗\n  ║   ║\n  ☹   ║\n /║\\  ║\n / \\  ║\n      ║\n  ════╩═══"
}

# 4. ESTRUCTURA DE LA APP
c1, c2 = st.columns([0.85, 0.15])
c1.markdown("## 🕹️ AHORCADO ONLINE")
if c2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    pi = st.text_input("🔑 ELIGE LA PALABRA:", type="password")
    if st.button("🚀 EMPEZAR PARTIDA", use_container_width=True):
        if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if won: st.balloons(); st.markdown("### 🏆 ¡LO LOGRASTE!")
        else: st.markdown(f"### 💀 FIN DEL JUEGO<br>ERA: **{s['p'].upper()}**", unsafe_allow_html=True)
        if st.button("🔄 NUEVA PARTIDA", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Layout Vertical
        st.markdown(f"""<div style='text-align:center;'>
            <div class='card'>
                <pre class='hangman-frame'>{stages[s['v']]}</pre>
                <div style='margin-top:10px; font-weight:bold;'>VIDAS: {s['v']} / 6</div>
                <div class='word-display'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        # Teclado (Con el estilo de borde solicitado)
        st.write("---")
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                l_low = l.lower()
                if l_low in s["u"]:
                    icon = "✅" if l_low in s["p"] else "❌"
                    st.markdown(f"<div style='text-align:center;'>{icon}<br><b>{l}</b></div>", unsafe_allow_html=True)
                elif st.button(l, key=f"key-{l}"):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        # Arriesgar
        st.write("")
        if st.button("🔥 ARRIESGAR TODO", use_container_width=True): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("🎯 ESCRIBE LA PALABRA:", key="guess").lower().strip()
            if st.button("✔️ ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
