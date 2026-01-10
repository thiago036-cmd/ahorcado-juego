import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Ahorcado Realtime", layout="centered")

# --- MEMORIA COMPARTIDA (Sincroniza a todos los jugadores) ---
@st.cache_resource
def obtener_estado_global():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

# 's' es el mismo objeto para todos los usuarios que entren al link
s = obtener_estado_global()

# --- ESTILOS VISUALES ---
st.markdown("""
    <style>
    .palabra-display { font-size: 40px; font-weight: bold; color: #FFD700; text-align: center; letter-spacing: 10px; margin: 20px 0; font-family: monospace; }
    .vidas-display { font-size: 26px; font-weight: bold; color: #FF4B4B; text-align: center; margin-bottom: 10px; }
    .stButton > button { width: 100%; height: 50px; font-size: 18px !important; font-weight: bold; }
    pre { background-color: #111 !important; color: #00FF00 !important; font-size: 20px !important; line-height: 1.1; }
    </style>
    """, unsafe_allow_html=True)

def reiniciar_juego():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

def dibujo_ahorcado(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | \n=======", # 0 vidas
        " +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | \n=======", # 1 vida
        " +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | \n=======", # 2 vidas
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======", # 3 vidas
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======", # 4 vidas
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======", # 5 vidas
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n======="  # 6 vidas
    ]
    return etapas[i]

# --- LÓGICA DE PARTIDA ---
if s["palabra"]:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    perdido = s["intentos"] <= 0

    if ganado:
        st.success(f"🏆 ¡GANAMOS! La palabra era: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar_juego)
    elif perdido:
        st.error(f"💀 PERDIMOS. La palabra era: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar_juego)
    else:
        # --- JUEGO EN CURSO ---
        st.markdown(f"<div class='vidas-display'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)
        
        col_dibujo, col_input = st.columns([1, 1])
        with col_dibujo:
            st.code(dibujo_ahorcado(s["intentos"]))
        with col_input:
            intento_palabra = st.text_input("🎯 ¿Sabes la palabra?", key="input_global").lower().strip()
            if st.button("ADIVINAR"):
                if intento_palabra == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()

        # Mostrar la palabra con guiones
        mostrar = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-display'>{mostrar}</div>", unsafe_allow_html=True)

        # Teclado con Ñ (7 columnas fijas para móvil)
        st.write("Selecciona una letra:")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["usadas"]:
                    # Muestra si acertaron o fallaron esa letra
                    st.write("✅" if l_min in s["palabra"] else "❌")
                else:
                    if st.button(letra, key=f"btn-{letra}"):
                        s["usadas"].append(l_min)
                        if l_min not in s["palabra"]: s["intentos"] -= 1
                        st.rerun()

    # REFRESCO AUTOMÁTICO: Cada 2 segundos revisa si otro jugador hizo un movimiento
    time.sleep(2)
    st.rerun()

else:
    # --- PANTALLA DE INICIO (SALA DE ESPERA) ---
    st.title("🏹 Ahorcado Online Realtime")
    st.write("Cualquiera que entre a este link verá lo mismo que tú.")
    nueva_p = st.text_input("Escribe la palabra secreta para todos:", type="password")
    if st.button("🚀 INICIAR PARTIDA"):
        if nueva_p:
            s.update({"palabra": nueva_p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
