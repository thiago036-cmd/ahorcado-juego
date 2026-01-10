import streamlit as st
import time

# --- CONFIGURACIÓN Y MEMORIA ONLINE ---
st.set_page_config(page_title="Ahorcado Realtime", layout="centered")

@st.cache_resource
def obtener_estado():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "tema": "oscuro"}

s = obtener_estado()

# --- INTERFAZ DE TEMA (CLARO/OSCURO) ---
if st.button(f"Cambiar a Modo {'Claro' if s['tema'] == 'oscuro' else 'Oscuro'}"):
    s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
    st.rerun()

# --- CSS PARA FORZAR COLUMNAS EN MÓVIL Y TEMAS ---
bgcolor = "#0E1117" if s["tema"] == "oscuro" else "#FFFFFF"
textcolor = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {bgcolor}; color: {textcolor}; }}
    
    /* FORZAR 7 COLUMNAS EN CELULAR (SIN APILAR) */
    [data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
    }}
    [data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    .palabra {{ font-size: 35px; font-weight: bold; color: #FFD700; text-align: center; letter-spacing: 5px; }}
    .vidas {{ font-size: 24px; font-weight: bold; color: #FF4B4B; text-align: center; }}
    .stButton > button {{ width: 100%; height: 45px; font-size: 16px; font-weight: bold; padding: 0; }}
    pre {{ background-color: #111 !important; color: #00FF00 !important; font-size: 16px !important; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False})
    st.rerun()

def dibujo(i):
    etapas = [" +---+ \n |   | \n O   | \n/|\\  | \n/ \\  | \n     | \n=======", " +---+ \n |   | \n O   | \n/|\\  | \n/    | \n     | \n=======", " +---+ \n |   | \n O   | \n/|\\  | \n     | \n     | \n=======", " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======", " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======", " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======", " +---+ \n |   | \n     | \n     | \n     | \n     | \n======="]
    return etapas[i]

# --- LÓGICA DE JUEGO ---
if not s["palabra"]:
    st.title("🏹 Sala Online")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    if ganado:
        st.success(f"🏆 ¡VICTORIA! PALABRA: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar)
    elif s["intentos"] <= 0:
        st.error(f"💀 PERDIDA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # Pantalla de juego
        st.markdown(f"<div class='vidas'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1: st.code(dibujo(s["intentos"]))
        with c2:
            adv = st.text_input("🎯 ¿La sabes?", key="adv").lower().strip()
            if st.button("ADIVINAR"):
                if adv == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()

        txt = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra'>{txt}</div>", unsafe_allow_html=True)

        # Teclado (Forzado 7 columnas para celular)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            cols = st.columns(7)
            fila = abc[i:i+7]
            for j, letra in enumerate(fila):
                l_min = letra.lower()
                with cols[j]:
                    if l_min in s["usadas"]:
                        st.write("✅" if l_min in s["palabra"] else "❌")
                    else:
                        if st.button(letra, key=f"k-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()
        
        time.sleep(2)
        st.rerun()
