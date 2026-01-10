import streamlit as st
from streamlit_autorefresh import st_autorefresh

# --- CONFIGURACIÓN DEL SERVIDOR (MEMORIA COMPARTIDA) ---
@st.cache_resource
def obtener_servidor():
    return {
        "palabra": "",
        "usadas": [],
        "intentos": 6,
        "gano_directo": False
    }

srv = obtener_servidor()

# Configuración de página
st.set_page_config(page_title="Ahorcado Realtime Pro", layout="centered")

# AUTO-REFRESCO: Actualiza la pantalla de todos cada 2000ms (2 segundos)
st_autorefresh(interval=2000, key="datarefresh")

# Estilos visuales
st.markdown("""
    <style>
    .word-box { font-size: 45px; letter-spacing: 12px; text-align: center; margin: 20px; color: white; background: #333; border-radius: 15px; padding: 10px; font-weight: bold; }
    .stButton > button { width: 100%; border-radius: 8px; height: 50px; font-size: 18px; font-weight: bold; }
    code { font-size: 1.3em !important; color: #ffcc00 !important; line-height: 1.1; }
    </style>
    """, unsafe_allow_html=True)

def dibujo(i):
    etapas = [
        """ +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | """, # 0
        """ +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | """, # 1
        """ +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | """, # 2
        """ +---+ \n |   | \n O   | \n/|   | \n     | \n     | """, # 3
        """ +---+ \n |   | \n O   | \n |   | \n     | \n     | """, # 4
        """ +---+ \n |   | \n O   | \n     | \n     | \n     | """, # 5
        """ +---+ \n |   | \n     | \n     | \n     | \n     | """  # 6
    ]
    return etapas[i]

# --- LÓGICA DE SALA ---
if not srv["palabra"]:
    st.title("🎮 Nueva Sala Multijugador")
    st.write("Cualquiera que entre puede poner la palabra.")
    p_secreta = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 INICIAR JUEGO PARA TODOS"):
        if p_secreta:
            srv["palabra"] = p_secreta.lower().strip()
            srv["usadas"] = []
            srv["intentos"] = 6
            srv["gano_directo"] = False
            st.rerun()

else:
    st.title("🗡️ Ahorcado en Tiempo Real")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        st.code(dibujo(srv["intentos"]))
    with col2:
        st.metric("Vidas", srv["intentos"])
        # Solo para palabra completa
        adivina_todo = st.text_input("¿La sabes?", placeholder="Palabra completa...", key="guess_box").lower().strip()
        if st.button("🔥 ¡ADIVINAR!"):
            if adivina_todo:
                if adivina_todo == srv["palabra"]:
                    srv["gano_directo"] = True
                else:
                    srv["intentos"] = 0
                st.rerun()

    # Palabra sincronizada
    visual = "".join([l.upper() if l in srv["usadas"] or l == " " or srv["gano_directo"] else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado táctil
    st.write("---")
    cols = st.columns(7)
    for i, letra in enumerate("abcdefghijklmnopqrstuvwxyz"):
        with cols[i % 7]:
            if letra in srv["usadas"]:
                label = "✅" if letra in srv["palabra"] else "❌"
                st.button(label, key=f"btn-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"btn-{letra}"):
                    srv["usadas"].append(letra)
                    if letra not in srv["palabra"]:
                        srv["intentos"] -= 1
                    st.rerun()

    # Final del juego
    ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"]
    
    if ganado or srv["intentos"] <= 0:
        if ganado:
            st.balloons()
            st.success(f"¡VICTORIA! Era: {srv['palabra'].upper()}")
        else:
            st.error(f"¡PERDIERON! La palabra era: {srv['palabra'].upper()}")
        
        if st.button("🔄 Reiniciar Sala"):
            srv["palabra"] = ""
            st.rerun()
