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

st.set_page_config(page_title="Ahorcado Pro Online", layout="centered")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .word-box { font-size: 50px; letter-spacing: 15px; text-align: center; margin: 20px; color: #FFD700; background: #262730; border-radius: 15px; padding: 20px; border: 2px solid #444; font-family: 'Courier New', Courier, monospace; }
    .stButton > button { width: 100%; border-radius: 10px; height: 55px; font-weight: bold; border: 1px solid #555; }
    
    /* Pantallas Finales con animaciones simples */
    .pantalla-victoria { background: linear-gradient(135deg, #28a745, #1e7e34); color: white; padding: 60px; border-radius: 30px; text-align: center; border: 5px solid #ffffff; }
    .pantalla-derrota { background: linear-gradient(135deg, #dc3545, #a71d2a); color: white; padding: 60px; border-radius: 30px; text-align: center; border: 5px solid #ffffff; }
    .texto-grande { font-size: 50px; font-weight: 900; margin: 0; text-shadow: 2px 2px 4px #000; }
    .palabra-revelada { font-size: 30px; background: rgba(0,0,0,0.3); padding: 10px; border-radius: 10px; margin-top: 20px; display: inline-block; }
    
    /* Estilo para el dibujo */
    .dibujo-contenedor { background: #111; padding: 20px; border-radius: 15px; border-left: 5px solid #ffcc00; font-family: monospace; font-size: 22px; color: #eee; line-height: 1; }
    </style>
    """, unsafe_allow_html=True)

def obtener_muneco_pro(i):
    # Usamos caracteres de bloques y emojis para un mejor look
    etapas = [
        # 0: Muerto
        "  ╔═══╦  \n  ║   💀  \n  ║  /|\\  \n  ║  / \\  \n  ║       \n  ╩═══════",
        # 1: Una pierna
        "  ╔═══╦  \n  ║   😟  \n  ║  /|\\  \n  ║  /    \n  ║       \n  ╩═══════",
        # 2: Cuerpo y brazos
        "  ╔═══╦  \n  ║   😰  \n  ║  /|\\  \n  ║       \n  ║       \n  ╩═══════",
        # 3: Cuerpo y un brazo
        "  ╔═══╦  \n  ║   😨  \n  ║  /|   \n  ║       \n  ║       \n  ╩═══════",
        # 4: Tronco
        "  ╔═══╦  \n  ║   😧  \n  ║   |   \n  ║       \n  ║       \n  ╩═══════",
        # 5: Solo cabeza
        "  ╔═══╦  \n  ║   🤔  \n  ║       \n  ║       \n  ║       \n  ╩═══════",
        # 6: Vacio
        "  ╔═══╦  \n  ║       \n  ║       \n  ║       \n  ║       \n  ╩═══════"
    ]
    return etapas[i]

# --- LÓGICA DE ESTADO ---
ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"] if srv["palabra"] else False
perdido = srv["intentos"] <= 0

# --- PANTALLAS ---

if ganado:
    st.balloons()
    st.markdown(f"""
        <div class="pantalla-victoria">
            <p class="texto-grande">👑 ¡VICTORIA!</p>
            <div class="palabra-revelada">LA PALABRA ERA: {srv['palabra'].upper()}</div>
        </div>
    """, unsafe_allow_html=True)
    if st.button("✨ JUGAR OTRA VEZ ✨"):
        srv["palabra"] = ""
        st.rerun()

elif perdido:
    st.markdown(f"""
        <div class="pantalla-derrota">
            <p class="texto-grande">⚰️ GAME OVER</p>
            <div class="palabra-revelada">LA PALABRA ERA: {srv['palabra'].upper()}</div>
        </div>
    """, unsafe_allow_html=True)
    st.markdown(f"<pre style='font-size:25px; text-align:center; background:none; border:none; color:white;'>{obtener_muneco_pro(0)}</pre>", unsafe_allow_html=True)
    if st.button("🔄 INTENTAR DE NUEVO"):
        srv["palabra"] = ""
        st.rerun()

elif not srv["palabra"]:
    st.title("🏹 Sala de Ahorcado Online")
    p_secreta = st.text_input("Ingresa la palabra secreta (nadie la verá):", type="password")
    if st.button("🔥 CREAR SALA"):
        if p_secreta:
            srv.update({"palabra": p_secreta.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()

else:
    st.title("🗡️ Batalla en Tiempo Real")
    
    c1, c2 = st.columns([1, 1])
    with c1:
        st.markdown(f"<div class='dibujo-contenedor'><pre>{obtener_muneco_pro(srv['intentos'])}</pre></div>", unsafe_allow_html=True)
    with c2:
        st.metric("Vidas", srv["intentos"])
        adivina = st.text_input("¿Crees saber la palabra?", placeholder="Escribe aquí...").lower().strip()
        if st.button("🎯 ¡ADIVINAR TODO!"):
            if adivina == srv["palabra"]: srv["gano_directo"] = True
            else: srv["intentos"] = 0
            st.rerun()

    # Palabra
    p_visual = "".join([l.upper() if l in srv["usadas"] or l == " " else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{p_visual}</div>", unsafe_allow_html=True)

    # Teclado
    st.write("### Selecciona una letra:")
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(7)
    for i, letra in enumerate(abc):
        with cols[i % 7]:
            if letra in srv["usadas"]:
                label = "✅" if letra in srv["palabra"] else "❌"
                st.button(label, key=f"k-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"k-{letra}"):
                    srv["usadas"].append(letra)
                    if letra not in srv["palabra"]: srv["intentos"] -= 1
                    st.rerun()
