import streamlit as st

# --- CONFIGURACIÓN DE MEMORIA COMPARTIDA ---
# Esto hace que todos los que entren al link vean los mismos datos
@st.cache_resource
def obtener_estado_global():
    return {
        "palabra": "",
        "usadas": [],
        "intentos": 6,
        "gano_directo": False
    }

global_state = obtener_estado_global()

st.set_page_config(page_title="Ahorcado Sincronizado", layout="centered")

# Estilos visuales
st.markdown("""
    <style>
    .word-box { font-size: 45px; letter-spacing: 12px; text-align: center; margin: 20px; color: #ffffff; font-weight: bold; background: #333; border-radius: 15px; padding: 10px; }
    .stButton > button { width: 100%; border-radius: 8px; height: 45px; font-size: 18px; }
    </style>
    """, unsafe_allow_html=True)

def obtener_dibujo(intentos):
    etapas = [
        """ +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | """, # 0
        """ +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | """, # 1
        """ +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | """, # 2
        """ +---+ \n |   | \n O   | \n/|   | \n     | \n     | """, # 3
        """ +---+ \n |   | \n O   | \n |   | \n     | \n     | """, # 4
        """ +---+ \n |   | \n O   | \n     | \n     | \n     | """, # 5
        """ +---+ \n |   | \n     | \n     | \n     | \n     | """  # 6
    ]
    return etapas[intentos]

# --- PANTALLA DE INICIO ---
if not global_state["palabra"]:
    st.title("🎮 Configura la Partida (Global)")
    p_ingresada = st.text_input("JUGADOR 1: Escribe la palabra secreta:", type="password")
    if st.button("🚀 COMENZAR PARA TODOS"):
        if p_ingresada:
            global_state["palabra"] = p_ingresada.lower().strip()
            st.rerun()

# --- PANTALLA DE JUEGO ---
else:
    st.title("🗡️ Ahorcado Online")
    
    col_dibujo, col_info = st.columns([1, 1])
    with col_dibujo:
        st.code(obtener_dibujo(global_state["intentos"]))
    with col_info:
        st.metric("Vidas", global_state["intentos"])
        
        # CUADRO SOLO PARA PALABRA COMPLETA
        adivinanza = st.text_input("¿Sabes la palabra correcta?", key="input_global").lower().strip()
        
        if st.button("¡ADIVINAR!"):
            if adivinanza:
                if adivinanza == global_state["palabra"]:
                    global_state["gano_directo"] = True
                else:
                    global_state["intentos"] = 0
                st.rerun()

    # Palabra oculta
    progreso = "".join([l.upper() if l in global_state["usadas"] or l == " " or global_state["gano_directo"] else "_" for l in global_state["palabra"]])
    st.markdown(f"<div class='word-box'>{progreso}</div>", unsafe_allow_html=True)

    # Teclado de botones
    st.write("---")
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(9)
    for i, letra in enumerate(abc):
        with cols[i % 9]:
            if letra in global_state["usadas"]:
                label = "✅" if letra in global_state["palabra"] else "❌"
                st.button(label, key=f"btn-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"btn-{letra}"):
                    global_state["usadas"].append(letra)
                    if letra not in global_state["palabra"]:
                        global_state["intentos"] -= 1
                    st.rerun()

    # Final del Juego
    ganado = all(l in global_state["usadas"] or l == " " for l in global_state["palabra"]) or global_state["gano_directo"]
    
    if ganado or global_state["intentos"] <= 0:
        if ganado:
            st.success(f"¡VICTORIA! Palabra: {global_state['palabra'].upper()}")
        else:
            st.error(f"¡GAME OVER! Era: {global_state['palabra'].upper()}")
            
        if st.button("🔄 Reiniciar Servidor"):
            global_state["palabra"] = ""
            global_state["usadas"] = []
            global_state["intentos"] = 6
            global_state["gano_directo"] = False
            st.rerun()

    # Botón de refrescar (Útil para ver qué hizo el otro)
    if st.button("🔄 Ver jugadas de otros"):
        st.rerun()
