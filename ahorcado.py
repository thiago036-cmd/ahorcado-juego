import streamlit as st

# Configuración visual
st.set_page_config(page_title="Ahorcado Pro Online", layout="centered")

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

# --- INICIO: JUGADOR 1 ---
if not st.session_state.palabra:
    st.title("🎮 Configura la Partida")
    p_ingresada = st.text_input("Escribe la palabra secreta:", type="password", help="Tus amigos no verán lo que escribes")
    if st.button("🚀 EMPEZAR"):
        if p_ingresada:
            st.session_state.palabra = p_ingresada.lower().strip()
            st.rerun()

# --- JUEGO: JUGADORES ---
else:
    st.title("🗡️ Ahorcado")
    
    # Dibujo y Vidas
    col_dibujo, col_info = st.columns([1, 1])
    with col_dibujo:
        st.code(obtener_dibujo(st.session_state.intentos))
    with col_info:
        st.metric("Vidas", st.session_state.intentos)
        # ENTRADA DE TECLADO FÍSICO
        teclado = st.text_input("Usa tu teclado (escribe una letra y pulsa Enter):", value="", max_chars=1).lower()
        if teclado and teclado.isalpha():
            if teclado not in st.session_state.usadas:
                st.session_state.usadas.append(teclado)
                if teclado not in st.session_state.palabra:
                    st.session_state.intentos -= 1
                st.rerun()

    # Mostrar Palabra
    progreso = "".join([l.upper() if l in st.session_state.usadas or l == " " else "_" for l in st.session_state.palabra])
    st.markdown(f"<div class='word-box'>{progreso}</div>", unsafe_allow_html=True)

    # ARRIESGAR PALABRA COMPLETA
    with st.expander("🤔 ¿Sabes la palabra entera?"):
        arriesgar = st.text_input("Escribe la palabra completa:").lower().strip()
        if st.button("🔥 ¡ADIVINAR TODO!"):
            if arriesgar == st.session_state.palabra:
                st.session_state.usadas.extend(list(arriesgar))
            else:
                st.session_state.intentos = 0 # Castigo por fallar la palabra completa
            st.rerun()

    # TECLADO TÁCTIL (Botones)
    st.write("---")
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(9)
    for i, letra in enumerate(abc):
        with cols[i % 9]:
            if letra in st.session_state.usadas:
                color = "✅" if letra in st.session_state.palabra else "❌"
                st.button(color, key=f"btn-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"btn-{letra}"):
                    st.session_state.usadas.append(letra)
                    if letra not in st.session_state.palabra:
                        st.session_state.intentos -= 1
                    st.rerun()

    # FINAL DEL JUEGO
    ganado = all(l in st.session_state.usadas or l == " " for l in st.session_state.palabra)
    
    if ganado:
        st.balloons()
        st.success(f"¡VICTORIA! Era: {st.session_state.palabra.upper()}")
        if st.button("🔄 Nueva Partida"):
            st.session_state.palabra = ""; st.session_state.usadas = []; st.session_state.intentos = 6; st.rerun()
            
    elif st.session_state.intentos <= 0:
        st.error(f"¡PERDIERON! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("🔄 Reintentar"):
            st.session_state.palabra = ""; st.session_state.usadas = []; st.session_state.intentos = 6; st.rerun()
