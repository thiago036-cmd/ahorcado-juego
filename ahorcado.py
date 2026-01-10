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

# Auto-refresco cada 2 segundos
st_autorefresh(interval=2000, key="datarefresh")

st.set_page_config(page_title="Ahorcado Pro Online", layout="centered")

# --- CSS PARA ALINEACIÓN PERFECTA ---
st.markdown("""
    <style>
    .dibujo-container {
        position: relative;
        font-family: 'Courier New', Courier, monospace;
        background-color: #111;
        color: #eee;
        padding: 20px;
        border-radius: 10px;
        font-size: 24px;
        line-height: 1.2;
        width: 200px;
        height: 220px;
        border: 2px solid #444;
        margin: auto;
    }
    .emoji-cabeza {
        position: absolute;
        left: 68px; /* Ajuste preciso para centrar la cabeza */
        top: 55px;
        font-size: 24px;
        line-height: 1;
    }
    .horca-base {
        white-space: pre;
    }
    .word-box { 
        font-size: 45px; letter-spacing: 10px; text-align: center; 
        margin: 20px 0; color: #FFD700; background: #262730; 
        border-radius: 15px; padding: 15px; font-family: monospace;
    }
    .v-bg { background-color: #28a745; padding: 60px 20px; border-radius: 20px; text-align: center; color: white; }
    .d-bg { background-color: #dc3545; padding: 60px 20px; border-radius: 20px; text-align: center; color: white; }
    </style>
    """, unsafe_allow_html=True)

def mostrar_dibujo(intentos):
    # Caras según intentos
    caras = {0:"💀", 1:"😰", 2:"😨", 3:"😧", 4:"🤔", 5:"🙂"}
    c = caras.get(intentos, "")
    
    # El cuerpo se dibuja con espacios vacíos donde va la cabeza
    cuerpos = [
        "  +---+  \n  |   |  \n      |  \n /\\  |  \n / \  |  \n      |  \n=========", # 0
        "  +---+  \n  |   |  \n      |  \n /|\  |  \n /    |  \n      |  \n=========", # 1
        "  +---+  \n  |   |  \n      |  \n /|\  |  \n      |  \n      |  \n=========", # 2
        "  +---+  \n  |   |  \n      |  \n /|   |  \n      |  \n      |  \n=========", # 3
        "  +---+  \n  |   |  \n      |  \n  |   |  \n      |  \n      |  \n=========", # 4
        "  +---+  \n  |   |  \n      |  \n      |  \n      |  \n      |  \n=========", # 5
        "  +---+  \n  |   |  \n      |  \n      |  \n      |  \n      |  \n========="  # 6
    ]
    
    html_dibujo = f"""
    <div class="dibujo-container">
        <div class="emoji-cabeza">{c}</div>
        <div class="horca-base">{cuerpos[intentos]}</div>
    </div>
    """
    return html_dibujo

# --- LÓGICA ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

if ganado:
    st.markdown(f'<div class="v-bg"><h1>✨ ¡GANASTE!</h1><p>La palabra era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    if st.button("NUEVA PARTIDA"): srv["palabra"] = ""; st.rerun()
elif perdido:
    st.markdown(f'<div class="d-bg"><h1>💀 PERDISTE</h1><p>La palabra era: {srv["palabra"].upper()}</p></div>', unsafe_allow_html=True)
    st.markdown(mostrar_dibujo(0), unsafe_allow_html=True)
    if st.button("REINTENTAR"): srv["palabra"] = ""; st.rerun()
elif not srv["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("EMPEZAR"):
        if p:
            srv.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    st.title("🗡️ Ahorcado Online")
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(mostrar_dibujo(srv["intentos"]), unsafe_allow_html=True)
    with c2:
        st.metric("Vidas", srv["intentos"])
        adivina = st.text_input("¿La sabes?", key="guess").lower().strip()
        if st.button("ADIVINAR"):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

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
