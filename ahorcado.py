import streamlit as st
from streamlit_autorefresh import st_autorefresh

# 1. ESTADO Y CONFIGURACIÓN
st.set_page_config(page_title="Ahorcado Online", layout="centered")
@st.cache_resource
def engine(): return {"p": "", "u": [], "v": 6, "win": False, "bet": False, "dark": True}

s = engine()
st_autorefresh(interval=2000, key="sync")

# 2. ESTILO COMPACTO
bg, cd, tx, br = ("#0e1117","#161b22","#fff","#30363d") if s["dark"] else ("#fff","#f6f8fa","#1f2328","#d0d7de")
st.markdown(f"""<style>
    .stApp {{ background:{bg}; color:{tx}; font-family: sans-serif; }}
    .card {{ background:{cd}; border:1px solid {br}; border-radius:12px; padding:20px; text-align:center; }}
    .draw {{ font-family:monospace; font-size:18px; background:#000; color:#39ff14; padding:10px; border-radius:8px; display:inline-block; }}
    .word {{ font-size:35px; font-weight:800; letter-spacing:10px; margin:15px 0; }}
    div[data-testid="column"] button {{ background:{cd}!important; color:{tx}!important; border:1px solid {br}!important; height:40px!important; }}
    .stButton > button[key="th"] {{ background:#58a6ff!important; color:#fff!important; }}
</style>""", unsafe_allow_html=True)

# 3. LÓGICA Y DIBUJO
stages = ["  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n===", "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n===", "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n===", "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n===", "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n===", "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n===", "  +---+\n  |   |\n      |\n      |\n      |\n      |\n==="]

c1, c2 = st.columns([0.8, 0.2])
c1.title("AHORCADO ONLINE")
if c2.button("🌓", key="th"): s["dark"] = not s["dark"]; st.rerun()

if not s["p"]:
    with st.container():
        pi = st.text_input("Palabra secreta:", type="password")
        if st.button("JUGAR"): s.update({"p":pi.lower().strip(),"u":[],"v":6,"win":False}); st.rerun()
else:
    won = all(l in s["u"] or l == " " for l in s["p"]) or s["win"]
    if won or s["v"] <= 0:
        st.markdown(f"<div class='card'>{'🏆 GANASTE' if won else '💀 PERDISTE'}<br>ERA: {s['p'].upper()}</div>", unsafe_allow_html=True)
        if st.button("REINICIAR"): s.update({"p":""}); st.rerun()
    else:
        st.markdown(f"<div class='card'><pre class='draw'>{stages[s['v']]}</pre><div class='word'>{' '.join([l.upper() if l in s['u'] or l==' ' else '_' for l in s['p']])}</div></div>", unsafe_allow_html=True)
        
        # Teclado
        cols = st.columns(7)
        for i, l in enumerate("ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"):
            with cols[i%7]:
                if l.lower() in s["u"]:
                    cl = "#238636" if l.lower() in s["p"] else "#6e7681"
                    st.markdown(f"<p style='text-align:center;color:{cl};font-weight:bold;'>{l}</p>", unsafe_allow_html=True)
                elif st.button(l, key=l):
                    s["u"].append(l.lower())
                    if l.lower() not in s["p"]: s["v"] -= 1
                    st.rerun()
        
        # Arriesgar
        if st.button("🔥 ARRIESGAR", key="arr"): s["bet"] = not s["bet"]; st.rerun()
        if s["bet"]:
            ans = st.text_input("Respuesta:").lower().strip()
            if st.button("ENVIAR"): 
                if ans == s["p"]: s["win"] = True
                else: s["v"] = 0
                st.rerun()
