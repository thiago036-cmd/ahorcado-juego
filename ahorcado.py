import streamlit as st

# Configuración de la página para que se vea bien en celular
st.set_page_config(page_title="El Ahorcado Pro", layout="centered")

# Estilos de color personalizados
st.markdown("""
    <style>
    .correct { color: #2ecc71; font-weight: bold; font-size: 20px; }
    .incorrect { color: #e74c3c; text-decoration: line-through; margin-right: 5px; }
    .unused { color: #3498db; margin-right: 5px; }
    .word-box { font-size: 40px; letter-spacing: 10px; text-align: center; margin: 20px; }
    </style>
    """, unsafe_allow_html=True)

def dibujar_ahorcado(intentos):
    etapas = [
        "💀 MUERTO", "😫 1 Intento", "😧 2 Intentos", 
        "🙁 3 Intentos", "😐 4 Intentos", "🙂 5 Intentos", "🌳 Inicio"
    ]
    return etapas[intentos]

# --- LÓGICA DE ESTADO (Para que la web no se reinicie sola) ---
if 'palabra' not in st.session_state:
    st.session_state.palabra = ""
    st.session_state.usadas = []
    st.session_state.intentos = 6

# --- FASE 1: CONFIGURACIÓN ---
if not st.session_state.palabra:
    st.title("🎮 Configuración del Juego")
    entrada = st.text_input("JUGADOR 1: Escribe la palabra secreta", type="password")
    if st.button("Empezar Juego"):
        if entrada:
            st.session_state.palabra = entrada.lower().strip()
            st.rerun()
else:
    # --- FASE 2: EL JUEGO ---
    st.title("🗡️ Ahorcado Online")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader(dibujar_ahorcado(st.session_state.intentos))
        
    with col2:
        st.metric("Vidas", st.session_state.intentos)

    # Mostrar Palabra
    progreso = ""
    for letra in st.session_state.palabra:
        if letra == " ": progreso += "  "
        elif letra in st.session_state.usadas: progreso += letra.upper()
        else: progreso += "_"
    
    st.markdown(f"<div class='word-box'>{progreso}</div>", unsafe_allow_html=True)

    # Teclado en pantalla (Ideal para celular)
    st.write("### Toca una letra:")
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(7) # 7 letras por fila para que quepa en móvil
    
    for i, letra in enumerate(abc):
        with cols[i % 7]:
            if letra in st.session_state.usadas:
                color = "✅" if letra in st.session_state.palabra else "❌"
                st.button(color, key=letra, disabled=True)
            else:
                if st.button(letra.upper(), key=letra):
                    st.session_state.usadas.append(letra)
                    if letra not in st.session_state.palabra:
                        st.session_state.intentos -= 1
                    st.rerun()

    # Opción de adivinar palabra completa
    adivina = st.text_input("¿Sabes la palabra entera?", key="adivina").lower().strip()
    if st.button("Arriesgar Palabra"):
        if adivina == st.session_state.palabra:
            st.session_state.usadas.extend(list(adivina))
        else:
            st.session_state.intentos = 0
        st.rerun()

    # --- FINAL DEL JUEGO ---
    ganado = all(l in st.session_state.usadas or l == " " for l in st.session_state.palabra)
    
    if ganado:
        st.success(f"¡VICTORIA! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("Nueva Partida"):
            st.session_state.palabra = ""
            st.session_state.usadas = []
            st.session_state.intentos = 6
            st.rerun()
            
    if st.session_state.intentos <= 0:
        st.error(f"¡GAME OVER! La palabra era: {st.session_state.palabra.upper()}")
        if st.button("Reintentar"):
            st.session_state.palabra = ""
            st.session_state.usadas = []
            st.session_state.intentos = 6
            st.rerun()