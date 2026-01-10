import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. CONFIGURACIÓN Y ESTADO
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. ESTILO VERTICAL Y LIMPIO
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: sans-serif; }}
    .v-stack {{ display: flex; flex-direction: column; align-items: center; gap: 15px; }}
    .card {{ background:{cd}; border:1px solid {br}; border-radius:12px; padding:20px; width: 100%; text-align:center; }}
    .draw-box {{ font-family:monospace; font-size:18px; background:#000; color:#39ff14; padding:15px; border-radius:10px; line-height:1.1; display:inline-block; text-align:left; }}
    .word {{ font-size:32px; font-weight:800; letter-spacing:8px; margin:15px 0; color:#58a6ff; }}
    div[data-testid="column"] button {{ background:{cd}!important; color:{tx}!important; border:1px solid {br}!important; height:42px!important; padding:0!important; }}
</style>""", unsafe_allow_html=True)

# 3. DIBUJO DEL MUÑECO
stages = [
    "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
    "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
    "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
]

# 4. INTERFAZ
c1, c2 = st.columns([0.9, 0.1])
c1.title("AHORCADO ONLINE")
if c2.button("🌓"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    with st.container():
        pi = st.text_input("Palabra secreta:", type="password")
        if st.button("EMPEZAR PARTIDA", use_container_width=True):
            if pi: s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown(f"<div class='card'>{'🏆 ¡GANASTE!' if won else '💀 PERDISTE'}<br>ERA: {s['p'].upper()}</div>", unsafe_allow_html=True)
        if st.button("NUEVA PARTIDA", use_container_width=True): s.update({"p":""}); st.rerun()
    else:
        # Layout Vertical
        st.markdown(f"""<div class='v-stack'>
            <div class='card'><pre class='draw-box'>{stages[s['v']]}</pre>
            <div style='font-weight:bold; margin-top:10px;'>Vidas: {s['v']} / 6</div>
            <div class='word'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div></div>
        </div>""", unsafe_allow_html=True)
        
        # Teclado (Letras horizontales)
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                if l.lower() in s["u"]:
                    cl = "#238636" if l.lower() in s["p"] else "#6e7681"
                    st.markdown(f"<p style='text-align:center;color:{cl};font-weight:bold;margin:5px 0;'>{l}</p>", unsafe_allow_html=True)
                elif st.button(l, key=l):
                    s["u"].append(l.lower())
                    if l.lower() not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        # Arriesgar
        st.write("---")
        if st.button("🔥 ARRIESGAR TODO", use_container_width=True): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("Escribe la palabra:").lower().strip()
            if st.button("ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
