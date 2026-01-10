import streamlit as st

# Título con estilo
st.title("🗡️ AHORCADO MULTIJUGADOR ONLINE")

# --- CONEXIÓN DE DATOS ---
# Usamos st.cache_resource para simular una "sala" común para todos
if "sala_comun" not in st.session_state:
    st.session_state["sala_comun"] = {
        "palabra": "",
        "letras_adivinadas": [],
        "intentos": 6,
        "estado": "esperando" # puede ser 'jugando' o 'terminado'
    }

sala = st.session_state["sala_comun"]

# --- LÓGICA PARA EL ANFITRIÓN (El que pone la palabra) ---
with st.sidebar:
    st.header("⚙️ Panel de Control")
    if st.button("🔄 Reiniciar Partida"):
        sala["palabra"] = ""
        sala["letras_adivinadas"] = []
        sala["intentos"] = 6
        sala["estado"] = "esperando"
        st.rerun()

if sala["estado"] == "esperando":
    st.info("Esperando a que alguien ponga una palabra...")
    nueva_palabra = st.text_input("JUGADOR 1: Pon la palabra secreta", type="password")
    if st.button("Crear Partida"):
        if nueva_palabra:
            sala["palabra"] = nueva_palabra.lower().strip()
            sala["estado"] = "jugando"
            st.rerun()

# --- LÓGICA PARA LOS JUGADORES (Los que adivinan) ---
else:
    st.write(f"### Vidas restantes: {'❤️' * sala['intentos']}")
    
    # Mostrar la palabra oculta
    progreso = ""
    for letra in sala["palabra"]:
        if letra == " ": progreso += "  "
        elif letra in sala["letras_adivinadas"]: progreso += letra.upper() + " "
        else: progreso += "_ "
    
    st.markdown(f"## {progreso}")

    # Teclado táctil
    abc = "abcdefghijklmnopqrstuvwxyz"
    cols = st.columns(9)
    for i, letra in enumerate(abc):
        with cols[i % 9]:
            if letra in sala["letras_adivinadas"]:
                st.button(letra.upper(), key=f"btn-{letra}", disabled=True)
            else:
                if st.button(letra.upper(), key=f"btn-{letra}"):
                    sala["letras_adivinadas"].append(letra)
                    if letra not in sala["palabra"]:
                        sala["intentos"] -= 1
                    st.rerun()

    # Comprobar si ganaron o perdieron
    palabra_limpia = sala["palabra"].replace(" ", "")
    if all(l in sala["letras_adivinadas"] for l in palabra_limpia):
        st.balloons()
        st.success("¡GANARON LA PARTIDA!")
        sala["estado"] = "terminado"
    
    if sala["intentos"] <= 0:
        st.error(f"¡PERDIERON! La palabra era: {sala['palabra'].upper()}")
        sala["estado"] = "terminado"