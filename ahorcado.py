import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Online Pro", layout="centered")

# --- CEREBRO ONLINE ---
@st.cache_resource
def obtener_juego():
    return {
        "palabra": "", 
        "usadas": [], 
        "intentos": 6, 
        "gano_directo": False,
        "tema": "oscuro",
        "arriesgando": False
    }

s = obtener_juego()

# --- CSS DEFINITIVO ---
fondo = "#0E1117" if s["tema"] == "oscuro" else "#FFFFFF"
texto = "#FFFFFF" if s["tema"] == "oscuro" else "#000000"
btn_fondo = "#262730" if s["tema"] == "oscuro" else "#F0F2F6"
borde_color = "#444444" if s["tema"] == "oscuro" else "#CCCCCC"

# Calculamos el tamaño de la fuente según el largo de la palabra para que no salte de línea
largo_p = len(s["palabra"]) if s["palabra"] else 1
tamanio_fuente = "35px" if largo_p < 8 else "25px" if largo_p < 12 else "18px"

st.markdown(f"""
    <style>
    .stApp {{ background-color: {fondo}; color: {texto}; }}
    
    /* TECLADO 7 COLUMNAS FIJO */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 3px !important;
    }}
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 0% !important;
        min-width: 0px !important;
    }}

    /* BOTONES */
    .stButton > button {{
        width: 100% !important;
        height: 50px !important;
        font-weight: bold !important;
        background-color: {btn_fondo} !important;
        color: {texto} !important;
        border: 3px solid {borde_color} !important; 
        border-radius: 10px !important;
        font-size: 16px !important;
    }}

    /* BOTÓN ARRIESGAR */
    div.stButton > button[kind="secondary"] {{
        border: 3px solid #FF8C00 !important;
        color: #FF8C00 !important;
    }}

    /* MUÑECO CENTRADO */
    .dibujo-box {{ display: flex; justify-content: center; width: 100%; }}
    pre {{
        background-color: #1a1a1a !important;
        color: #00FF00 !important;
        font-size: 18px !important;
        line-height: 1.1 !important;
        padding: 10px !important;
        border: 2px solid {borde_color};
        width: fit-content;
    }}

    /* PALABRA ELÁSTICA (NO SALTA DE LÍNEA) */
    .palabra-box {{ 
        font-size: {tamanio_fuente} !important; 
        font-weight: bold; 
        color: #FFD700; 
        text-align: center; 
        white-space: nowrap; /* Evita que la palabra se rompa en filas */
        overflow-x: auto;    /* Si es exageradamente larga, permite scroll horizontal */
        letter-spacing: 4px; 
        margin: 15px 0; 
        font-family: monospace; 
    }}

    .vidas-box {{ font-size: 22px; font-weight: bold; color: #FF4B4B; text-align: center; }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False})
    st.rerun()

def dibujo_ascii(i):
    etapas = [
        " +---+ \n |   | \n O   | \n/|\  | \n/ \  | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|\  | \n/    | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|\  | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n/|   | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n |   | \n     | \n     | \n=======",
        " +---+ \n |   | \n O   | \n     | \n     | \n     | \n=======",
        " +---+ \n |   | \n     | \n     | \n     | \n     | \n=======" 
    ]
    return etapas[i]

if not s["palabra"]:
    st.title("🏹 Sala Online")
    if st.button("🌓 Tema"):
        s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
        st.rerun()
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "gano_directo": False})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado:
        st.balloons()
        st.success(f"🏆 ¡VICTORIA! ERA: {s['palabra'].upper()}")
        st.button("🔄 OTRA PARTIDA", on_click=reiniciar)
    elif s["intentos"] <= 0:
        st.error(f"💀 DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # 1. MUÑECO
        st.markdown(f'<div class="dibujo-box"><pre>{dibujo_ascii(s["intentos"])}</pre></div>', unsafe_allow_html=True)

        # 2. VIDAS
        st.markdown(f"<div class='vidas-box'>Vidas: ❤️ {s['intentos']}</div>", unsafe_allow_html=True)

        # 3. PALABRA (Con CSS que evita las 3 filas)
        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f"<div class='palabra-box'>{visual}</div>", unsafe_allow_html=True)

        # 4. ARRIESGAR
        c1, c2 = st.columns([0.5, 0.5])
        with c2:
            if st.button("🔥 ARRIESGAR", kind="secondary"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()
        
        if s["arriesgando"]:
            adv = st.text_input("Palabra completa:", key="arr_in").lower().strip()
            if st.button("CONFIRMAR"):
                if adv == s["palabra"]: s["gano_directo"] = True
                else: s.update({"intentos": 0, "arriesgando": False})
                st.rerun()

        # 5. TECLADO
        st.write("Letras:")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            fila = abc[i:i+7]
            cols = st.columns(7)
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
        
        if st.button("🌓 Tema"):
            s["tema"] = "claro" if s["tema"] == "oscuro" else "oscuro"
            st.rerun()

        time.sleep(2)
        st.rerun()
