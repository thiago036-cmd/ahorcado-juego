import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO GLOBAL
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. ESTILO (CLEAN & VERTICAL)
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; text-align: center; gap: 10px; }}
    .card {{ background:{cd}; border:1px solid {br}; border-radius:16px; padding:20px; width: 100%; }}
    .hangman {{ font-family: monospace; font-size: 22px; background: #000; color: #39ff14; padding: 20px; border-radius: 12px; line-height: 1.1; display: inline-block; text-align: left; }}
    .word-box {{ font-size: 38px; font-weight: 800; letter-spacing: 12px; margin: 20px 0; color: #58a6ff; }}
    div[data-testid="column"] button {{ background:{cd}!important; color:{tx}!important; border:1px solid {br}!important; height:45px!important; }}
</style>""", unsafe_allow_html=True)

# 3. ETAPAS DEL MUÑECO (PROGRESIÓN REAL)
# El índice corresponde a las vidas restantes (0 a 6)
stages = {
    6: "  +---+\n  |   |\n      |\n      |\n      |\n      |\n=========",
    5: "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    4: "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    3: "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    2: "  +---+\n  |   |\n  O   |\n /|\  |\n      |\n      |\n=========",
    1: "  +---+\n  |   |\n  O   |\n /|\  |\n /    |\n      |\n=========",
    0: "  +---+\n  |   |\n  O   |\n /|\  |\n / \  |\n      |\n========="
}

# 4. INTERFAZ
col_h1, col_h2 = st.columns([0.85, 0.15])
col_h1.markdown("## 🕹️ AHORCADO ONLINE")
if col_h2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    with st.container():
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        pi = st.text_input("🔑 Palabra secreta:", type="password")
        if st.button("🚀 EMPEZAR", use_container_width=True):
            if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        if won: st.balloons(); st.success("🏆 ¡VICTORIA!")
        else: st.error(f"💀 GAME OVER. La palabra era: {s['p'].upper()}")
        if st.button("🔄 NUEVA PARTIDA", use_container_width=True): s.update({"p":""}); st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        # Visualización Vertical
        st.markdown(f"""<div class='v-stack'>
            <div class='card'>
                <pre class='hangman'>{stages[s['v']]}</pre>
                <div style='margin-top:10px; font-weight:bold;'>❤️ Vidas: {s['v']} / 6</div>
                <div class='word-box'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div>
            </div>
        </div>""", unsafe_allow_html=True)
        
        # Teclado
        st.markdown("---")
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                l_low = l.lower()
                if l_low in s["u"]:
                    icon = "🟢" if l_low in s["p"] else "❌"
                    st.markdown(f"<div style='text-align:center; font-size:12px;'>{icon}<br><b>{l}</b></div>", unsafe_allow_html=True)
                elif st.button(l, key=l):
                    s["u"].append(l_low)
                    if l_low not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        # Botón Arriesgar
        st.write("")
        if st.button("🔥 ARRIESGAR TODO", use_container_width=True): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("🎯 Tu respuesta:", key="ans_input").lower().strip()
            if st.button("✔️ ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
