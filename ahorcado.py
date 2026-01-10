import streamlit as st

# Configuración visual de la página
st.set_page_config(page_title="Ahorcado Online", layout="centered")

# Estilos CSS para mejorar la apariencia en móvil
st.markdown("""
    <style>
    .ahorcado-container { font-family: monospace; font-size: 20px; line-height: 1.2; background-color: #1e1e1e; padding: 20px; border-radius: 10px; color: #ffcc00; }
    .word-box { font-size: 45px; letter-spacing: 12px; text-align: center; margin: 20px; color: #ffffff; font-weight: bold; }
    div.stButton > button { width: 100%; border-radius: 5px; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

# Dibujos del muñequito (basado en el estilo que te gustó)
def obtener_dibujo(intentos):
    etapas = [
        # 0: Muerto
        """
           +-------+
           |       |
           |       O
           |      /|\\
           |      / \\
           |    [MORISTE]
        """,
        # 1: Un pie
        """
           +-------+
           |       |
           |       O
           |      /|\\
           |      / 
           |
        """,
        # 2: Cuerpo y brazos
        """
           +-------+
           |       |
           |       O
           |      /|\\
           |      
           |
        """,
        # 3: Cuerpo y un brazo
        """
           +-------+
           |       |
           |       O
           |      /|
           |      
           |
        """,
        # 4: Tronco
        """
           +-------+
           |       |
           |       O
           |       |
           |      
           |
        """,
        # 5: Cabeza
        """
           +-------+
           |       |
           |       O
           |      
           |      
           |
        """,
        # 6: Vacío
        """
           +-------+
           |       |
           |       
           |      
           |      
           |
        """
    ]
    return etapas[intentos]

# --- MANEJO DE ESTADO (MULTIJUGADOR SIMULADO) ---
if 'palabra' not in st.session_state:
    st.session_state.palabra = ""
    st.session_state.usadas = []
    st.session_state.intentos = 6

# --- PANTALLA DE INICIO (JUGADOR 1) ---
if not st.session_state.palabra:
    st.title("🎮 Configura la Partida")
    p_ingresada = st.text_input("Escribe la palabra secreta (se ocultará):", type="password")
    if st.button("🚀 COMENZAR JUEGO"):
        if p_ingresada:
            st.session_state.palabra = p_ingresada.lower().strip()
            st.rerun()

# --- PANTALLA DE JUEGO (JUGADORES) ---
else:
    st.title("🗡️ Ahorcado Pro")
    
    # Mostrar el dibujo del muñequito
    st.markdown(f"```\n{obtener_dibujo(st.session_state.intentos)}\n```")
    
    # Mostrar la palabra
    progreso = ""
    for letra in st.session_state.palabra:
        if letra == " ": progreso += "  "
        elif letra in st.session_state.usadas: progreso += letra.upper()
        else: progreso += "_"
    
    st.markdown(f"<div class='word-box'>{progreso}</div>", unsafe_allow_html=True)

    # Teclado para celular
    st.write("### Elige una letra:")
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(7) 
    
    for i, letra in enumerate(abc):
        with cols[i % 7]:
            if letra in st.session_state.usadas:
                label = "✅" if letra in st.session_state.palabra else "❌"
                st.button(label, key=f"btn-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"btn-{letra}"):
                    st.session_state.usadas.append(letra)
                    if letra not in st.session_state.palabra:
                        st.session_state.intentos -= 1
                    st.rerun()

    # Verificar final
    ganado = all(l in st.session_state.usadas or l == " " for l in st.session_state.palabra)
    
    if ganado:
        st.balloons()
        st.success(f"¡VICTORIA! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("🔄 Jugar otra vez"):
            st.session_state.palabra = ""
            st.session_state.usadas = []
            st.session_state.intentos = 6
            st.rerun()
            
    elif st.session_state.intentos <= 0:
        st.error(f"¡PERDIERON! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("🔄 Intentar de nuevo"):
            st.session_state.palabra = ""
            st.session_state.usadas = []
            st.session_state.intentos = 6
            st.rerun()