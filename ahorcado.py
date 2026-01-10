import streamlit as st

# Configuración visual
st.set_page_config(page_title="Ahorcado Pro", layout="centered")

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

# --- ESTADO DEL JUEGO ---
if 'palabra' not in st.session_state:
    st.session_state.palabra = ""
    st.session_state.usadas = []
    st.session_state.intentos = 6
    st.session_state.gano_directo = False

# --- INICIO: JUGADOR 1 ---
if not st.session_state.palabra:
    st.title("🎮 Configura la Partida")
    p_ingresada = st.text_input("JUGADOR 1: Escribe la palabra secreta:", type="password")
    if st.button("🚀 COMENZAR"):
        if p_ingresada:
            st.session_state.palabra = p_ingresada.lower().strip()
            st.rerun()

# --- JUEGO ---
else:
    st.title("🗡️ Ahorcado")
    
    col_dibujo, col_info = st.columns([1, 1])
    with col_dibujo:
        st.code(obtener_dibujo(st.session_state.intentos))
    with col_info:
        st.metric("Vidas", st.session_state.intentos)
        
        # EL CUADRO AHORA SOLO SIRVE PARA LA PALABRA COMPLETA
        adivinanza = st.text_input("¿Sabes la palabra correcta? Escríbela aquí:", key="input_palabra").lower().strip()
        
        if st.button("¡ADIVINAR!"):
            if adivinanza:
                if adivinanza == st.session_state.palabra:
                    st.session_state.gano_directo = True
                else:
                    st.session_state.intentos = 0 # Fallar la palabra entera mata al muñeco
                st.rerun()

    # Mostrar Palabra
    progreso = "".join([l.upper() if l in st.session_state.usadas or l == " " or st.session_state.gano_directo else "_" for l in st.session_state.palabra])
    st.markdown(f"<div class='word-box'>{progreso}</div>", unsafe_allow_html=True)

    # TECLADO TÁCTIL (Única forma de elegir letras)
    st.write("---")
    st.write("### Toca una letra para adivinar:")
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(9)
    for i, letra in enumerate(abc):
        with cols[i % 9]:
            if letra in st.session_state.usadas:
                label = "✅" if letra in st.session_state.palabra else "❌"
                st.button(label, key=f"btn-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"btn-{letra}"):
                    st.session_state.usadas.append(letra)
                    if letra not in st.session_state.palabra:
                        st.session_state.intentos -= 1
                    st.rerun()

    # FINAL DEL JUEGO
    ganado = all(l in st.session_state.usadas or l == " " for l in st.session_state.palabra) or st.session_state.gano_directo
    
    if ganado:
        st.balloons()
        st.success(f"¡VICTORIA! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("🔄 Nueva Partida"):
            st.session_state.palabra = ""; st.session_state.usadas = []; st.session_state.intentos = 6; st.session_state.gano_directo = False; st.rerun()
            
    elif st.session_state.intentos <= 0:
        st.error(f"¡PERDIERON! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("🔄 Reintentar"):
            st.session_state.palabra = ""; st.session_state.usadas = []; st.session_state.intentos = 6; st.session_state.gano_directo = False; st.rerun()
