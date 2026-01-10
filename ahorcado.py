import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {
        "palabra": "",
        "usadas": [],
        "intentos": 6,
        "gano_directo": False
    }

srv = obtener_servidor()

# Auto-refresco cada 2 segundos para sincronizar a todos
st_autorefresh(interval=2000, key="datarefresh")

st.set_page_config(page_title="Ahorcado Realtime Pro", layout="centered")

# --- CSS PARA EL DISEÑO ---
st.markdown("""
    <style>
    .dibujo-box {
        font-family: 'Courier New', Courier, monospace;
        background-color: #111;
        color: #eee;
        padding: 20px;
        border-radius: 10px;
        line-height: 1.3;
        font-size: 24px;
        white-space: pre;
        display: inline-block;
        border: 2px solid #444;
    }
    .word-box { 
        font-size: 45px; letter-spacing: 10px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 15px; font-family: monospace;
    }
    .v-bg { background-color: #28a745; padding: 80px 20px; border-radius: 20px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 80px 20px; border-radius: 20px; text-align: center; color: white; }
    .texto-final { font-size: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo_con_gestos(i):
    # Lista de caras según intentos restantes (6 a 0)
    caras = ["💀", "😰", "😨", "😧", "🤔", "🙂", ""]
    c = caras[i]
    
    etapas = [
        f"  +---+  \n  |   |  \n  {c}   |  \n /|\\  |  \n / \\  |  \n      |  \n=========", # 0: Muerto
        f"  +---+  \n  |   |  \n  {c}   |  \n /|\\  |  \n /    |  \n      |  \n=========", # 1
        f"  +---+  \n  |   |  \n  {c}   |  \n /|\\  |  \n      |  \n      |  \n=========", # 2
        f"  +---+  \n  |   |  \n  {c}   |  \n /|   |  \n      |  \n      |  \n=========", # 3
        f"  +---+  \n  |   |  \n  {c}   |  \n  |   |  \n      |  \n      |  \n=========", # 4
        f"  +---+  \n  |   |  \n  {c}   |  \n      |  \n      |  \n      |  \n=========", # 5
        f"  +---+  \n  |   |  \n      |  \n      |  \n      |  \n      |  \n========="  # 6: Vacío
    ]
    return etapas[i]

# --- LÓGICA ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.markdown(f'<div class="v-bg"><p class="texto-final">✨ ¡VICTORIA! ✨</p><p>Adivinaron: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    if st.button("NUEVA PARTIDA"): srv["palabra"] = ""; st.rerun()

elif perdido:
    st.markdown(f'<div class="d-bg"><p class="texto-final">💀 ¡PERDISTE! 💀</p><p>La palabra era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.markdown(f'<center><div class="dibujo-box">{obtener_dibujo_con_gestos(0)}</div></center>', unsafe_allow_html=True)
    if st.button("REINTENTAR"): srv["palabra"] = ""; st.rerun()

elif not srv["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("EMPEZAR"):
        if p:
            srv.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()

else:
    st.title("🗡️ Ahorcado en Vivo")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f'<div class="dibujo-box">{obtener_dibujo_con_gestos(srv["intentos"])}</div>', unsafe_allow_html=True)
    with c2:
        st.metric("Vidas", srv["intentos"])
        adivina = st.text_input("¿Sabes la palabra?", key="full_word").lower().strip()
        if st.button("ADIVINAR"):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado
    cols = st.columns(7)
    for i, l in enumerate("abcdefghijklmnopqrstuvwxyz"):
        with cols[i % 7]:
            if l in srv["usadas"]:
                st.button("✅" if l in srv["palabra"] else "❌", key=f"k-{l}", disabled=True)
            else:
                if st.button(l.upper(), key=f"k-{l}"):
                    srv["usadas"].append(l)
                    if l not in srv["palabra"]: srv["intentos"] -= 1
                    st.rerun()
