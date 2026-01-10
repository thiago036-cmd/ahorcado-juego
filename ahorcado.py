import streamlit as st

# --- MEMORIA COMPARTIDA (EL SERVIDOR) ---
# Esta función crea una sola "pizarra" para todos los que entren al link
@st.cache_resource
def obtener_servidor():
    return {
        "palabra": "",
        "usadas": [],
        "intentos": 6,
        "gano_directo": False
    }

# Conectamos a todos los usuarios a la misma memoria
srv = obtener_servidor()

st.set_page_config(page_title="Ahorcado Realtime", layout="centered")

# CSS para que se vea bien en celular
st.markdown("""
    <style>
    .word-box { font-size: 45px; letter-spacing: 12px; text-align: center; margin: 20px; color: white; background: #333; border-radius: 15px; padding: 10px; font-weight: bold; }
    .stButton > button { width: 100%; border-radius: 8px; height: 50px; font-size: 18px; }
    code { font-size: 1.2em !important; color: #ffcc00 !important; }
    </style>
    """, unsafe_allow_html=True)

def dibujo(i):
    etapas = [
        """ +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | """, # 0 (Muerto)
        """ +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | """, # 1
        """ +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | """, # 2
        """ +---+ \n |   | \n O   | \n/|   | \n     | \n     | """, # 3
        """ +---+ \n |   | \n O   | \n |   | \n     | \n     | """, # 4
        """ +---+ \n |   | \n O   | \n     | \n     | \n     | """, # 5
        """ +---+ \n |   | \n     | \n     | \n     | \n     | """  # 6 (Vacio)
    ]
    return etapas[i]

# --- LÓGICA DE SALA ---

if not srv["palabra"]:
    st.title("🎮 Crear Sala Online")
    p_secreta = st.text_input("Escribe la palabra para todos:", type="password")
    if st.button("🚀 INICIAR PARTIDA"):
        if p_secreta:
            srv["palabra"] = p_secreta.lower().strip()
            srv["usadas"] = []
            srv["intentos"] = 6
            srv["gano_directo"] = False
            st.rerun()

else:
    st.title("🗡️ Ahorcado en Vivo")
    
    # Dibujo y Vidas (Sincronizado)
    col1, col2 = st.columns([1, 1])
    with col1:
        st.code(dibujo(srv["intentos"]))
    with col2:
        st.metric("Vidas Restantes", srv["intentos"])
        
        # Cuadro solo para la palabra completa
        adivina_todo = st.text_input("¿Sabes la palabra?", placeholder="Escríbela aquí...").lower().strip()
        if st.button("🔥 ¡ADIVINAR TODO!"):
            if adivina_todo:
                if adivina_todo == srv["palabra"]:
                    srv["gano_directo"] = True
                else:
                    srv["intentos"] = 0
                st.rerun()

    # Mostrar progreso de la palabra
    visual = "".join([l.upper() if l in srv["usadas"] or l == " " or srv["gano_directo"] else "_" for l in srv["palabra"]])
    st.markdown(f"<div class='word-box'>{visual}</div>", unsafe_allow_html=True)

    # Teclado de botones (Tocar una letra la marca para todos)
    st.write("---")
    cols = st.columns(7)
    for i, letra in enumerate("abcdefghijklmnopqrstuvwxyz"):
        with cols[i % 7]:
            if letra in srv["usadas"]:
                btn_label = "✅" if letra in srv["palabra"] else "❌"
                st.button(btn_label, key=f"key-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"key-{letra}"):
                    srv["usadas"].append(letra)
                    if letra not in srv["palabra"]:
                        srv["intentos"] -= 1
                    st.rerun()

    # Botón para refrescar manualmente (por si acaso)
    if st.button("🔄 Actualizar pantalla"):
        st.rerun()

    # Final del juego
    ganado = all(l in srv["usadas"] or l == " " for l in srv["palabra"]) or srv["gano_directo"]
    
    if ganado or srv["intentos"] <= 0:
        if ganado:
            st.balloons()
            st.success(f"¡VICTORIA COLECTIVA! Era: {srv['palabra'].upper()}")
        else:
            st.error(f"¡TODOS PERDIERON! La palabra era: {srv['palabra'].upper()}")
        
        if st.button("🔄 Reiniciar Sala (Nueva Palabra)"):
            srv["palabra"] = ""
            st.rerun()
