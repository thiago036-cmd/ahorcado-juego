import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. MOTOR DE JUEGO Y ESTADO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. DISEÑO UI VERTICAL (PROFESIONAL)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: 'Segoe UI', sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; gap: 10px; }}
    .card {{ background:{cd}; border:1px solid {br}; border-radius:16px; padding:20px; width: 100%; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}
    .hangman {{ font-family: monospace; font-size: 20px; background: #000; color: #00ff88; padding: 15px; border-radius: 10px; line-height: 1; display: inline-block; }}
    .word-box {{ font-size: 38px; font-weight: 800; letter-spacing: 12px; margin: 15px 0; color: #58a6ff; text-transform: uppercase; }}
    div[data-testid="column"] button {{ background:{cd}!important; color:{tx}!important; border:1px solid {br}!important; height:45px!important; font-weight: bold!important; }}
    .stButton > button[key="th"] {{ background: #58a6ff!important; border: none!important; }}
</style>""", unsafe_allow_html=True)

# 3. DIBUJOS DEL AHORCADO
stages = [
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
]

# 4. INTERFAZ DE USUARIO
c1, c2 = st.columns([0.85, 0.15])
c1.markdown(f"## 🕹️ AHORCADO ONLINE")
if c2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        pi = st.text_input("🔑 Escribe la palabra secreta:", type="password")
        if st.button("🚀 INICIAR JUEGO", use_container_width=True):
            if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown(f"<div class='card'>", unsafe_allow_html=True)
        if won: st.balloons(); st.markdown("### 🏆 ¡VICTORIA EXCELENTE!")
        else: st.markdown(f"### 💀 FIN DEL JUEGO<br>La palabra era: **{s['p'].upper()}**", unsafe_allow_html=True)
        if st.button("🔄 JUGAR OTRA VEZ", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Área de Juego Vertical
        st.markdown(f"""<div class='v-stack'>
            <div class='card'>
                <pre class='hangman'>{stages[s['v']]}</pre>
                <div style='margin-top:10px; font-weight:bold; font-size:18px;'>❤️ Vidas: {s['v']} / 6</div>
                <div class='word-box'>{' '.join([l if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        # Teclado (Horizontal para comodidad)
        st.markdown("---")
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                l_low = l.lower()
                if l_low in s["u"]:
                    color = "🟢" if l_low in s["p"] else "❌"
                    st.markdown(f"<div style='text-align:center; font-size:12px;'>{color}<br><b>{l}</b></div>", unsafe_allow_html=True)
                elif st.button(l, key=l):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        # Arriesgar
        st.write("")
        if st.button("🔥 ARRIESGAR TODO", use_container_width=True, key="arr"): 
            s["bet"] = not s["bet"]; st.rerun()
        
        if s["bet"]:
            ans = st.text_input("🎯 Escribe la palabra completa:").lower().strip()
            if st.button("✔️ ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()

st.caption("Hecho con ❤️ para una experiencia Pro")
