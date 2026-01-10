import streamlit as st
import time

# --- ESTADO DEL JUEGO ---
if "srv" not in st.session_state:
    st.session_state.srv = {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}

s = st.session_state.srv

def reiniciar():
    st.session_state.srv = {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False}
    st.rerun()

# --- ESTILOS SIMPLES ---
st.markdown("""
    <style>
    .palabra { font-size: 35px; font-weight: bold; color: #FFD700; text-align: center; letter-spacing: 8px; }
    .vidas { font-size: 24px; font-weight: bold; color: #FF4B4B; }
    /* Botones estándar para que no se esconda la letra en móvil */
    .stButton > button { width: 100%; height: 50px; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

def dibujo(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======", 
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======", 
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n=======" 
    ]
    return etapas[i]

# --- PANTALLAS FINALES ---
ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"] if s["palabra"] else False

if ganado:
    st.balloons()
    st.success(f"🏆 ¡VICTORIA! LA PALABRA ERA: {s['palabra'].upper()}")
    st.button("🔄 JUGAR OTRA VEZ", on_click=reiniciar)
elif s["intentos"] <= 0:
    st.error(f"💀 PERDISTE. LA PALABRA ERA: {s['palabra'].upper()}")
    st.button("🔄 REINTENTAR", on_click=reiniciar)
elif not s["palabra"]:
    st.title("🏹 Ahorcado Online")
    p = st.text_input("Escribe la palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR JUEGO"):
        if p:
            s["palabra"] = p.lower().strip()
            st.rerun()
else:
    # --- INTERFAZ DE JUEGO ---
    c1, c2 = st.columns([1, 1])
    with c1:
        st.code(dibujo(s["intentos"]))
    with c2:
        st.markdown(f"<div class='vidas'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)
        adivina = st.text_input("🎯 ¿La sabes?", key="adv").lower().strip()
        if st.button("ADIVINAR"):
            if adivina == s["palabra"]: s["gano_directo"] = True
            else: s["intentos"] = 0
            st.rerun()

    # Palabra con guiones
    txt = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
    st.markdown(f"<p class='palabra'>{txt}</p>", unsafe_allow_html=True)

    # Teclado (7 columnas)
    st.write("Selecciona una letra:")
    abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
    cols = st.columns(7)
    for i, letra in enumerate(abc):
        l_min = letra.lower()
        with cols[i % 7]:
            if l_min in s["usadas"]:
                # Emoji de acierto o fallo
                st.write("✅" if l_min in s["palabra"] else "❌")
            else:
                if st.button(letra, key=f"k-{letra}"):
                    s["usadas"].append(l_min)
                    if l_min not in s["palabra"]: s["intentos"] -= 1
                    st.rerun()

    time.sleep(4)
    st.rerun()
