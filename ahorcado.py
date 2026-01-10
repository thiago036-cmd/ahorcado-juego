import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Pro Vertical", layout="centered")

@st.cache_resource
def obtener_juego():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "tema": "oscuro", "arriesgando": False}

s = obtener_juego()
color_alerta = "#00ff88" if s["intentos"] >= 4 else "#ffcc00" if s["intentos"] >= 2 else "#ff4444"

# --- CSS: VERTICALIDAD + BOTÓN ARRIESGAR ABAJO DERECHA ---
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; padding-bottom: 2rem !important; }}
    .stApp {{ background: #0f172a; color: white; }}

    /* 1. DIBUJO VERTICAL */
    .muneco-box {{
        background: #1a1a1a;
        border: 3px solid {color_alerta};
        border-radius: 20px;
        padding: 10px;
        width: fit-content;
        margin: 0 auto 10px auto;
    }}
    .muneco-texto {{
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
        color: {color_alerta} !important;
        white-space: pre !important;
        line-height: 1.1 !important;
    }}

    /* 2. VIDAS */
    .vidas-display {{ text-align: center; font-size: 20px; margin-bottom: 10px; font-weight: bold; }}

    /* 3. PALABRA */
    .palabra-box {{
        font-size: 9vw !important;
        font-weight: 900;
        color: #fbbf24;
        text-align: center;
        margin-bottom: 20px;
        letter-spacing: 4px;
    }}

    /* 4. TECLADO (HORIZONTAL 7 COLUMNAS) */
    div[data-testid="stHorizontalBlock"] button {{
        height: 48px !important;
        font-size: 16px !important;
        font-weight: 800 !important;
        border-radius: 8px !important;
        background: #1e293b !important;
        color: white !important;
        border: 3px solid #475569 !important;
    }}

    /* 5. BOTÓN ARRIESGAR (ESTILO ESPECIAL NARANJA) */
    .stButton > button[key*="btn-arr"] {{
        background: linear-gradient(135deg, #f39c12, #e67e22) !important;
        border: 2px solid white !important;
        color: white !important;
        font-weight: bold !important;
        height: 45px !important;
        border-radius: 10px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False})
    st.rerun()

def get_dibujo(i):
    etapas = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========",
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========",
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="
    ]
    return etapas[i]

# --- FLUJO ---
if not s["palabra"]:
    st.title("🎯 Crear Partida")
    p = st.text_input("Escribe la palabra secreta:", type="password")
    if st.button("🚀 EMPEZAR"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado or s["intentos"] <= 0:
        if ganado: st.balloons(); st.success("¡GANASTE!")
        else: st.error(f"DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar, use_container_width=True)
    else:
        # 1. Muñeco
        st.markdown(f'<div class="muneco-box"><div class="muneco-texto">{get_dibujo(s["intentos"])}</div></div>', unsafe_allow_html=True)

        # 2. Vidas
        st.markdown(f'<div class="vidas-display">❤️ {s["intentos"]} VIDAS</div>', unsafe_allow_html=True)

        # 3. Palabra Secreta
        v = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f'<div class="palabra-box">{v}</div>', unsafe_allow_html=True)

        # 4. Teclado
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            cols = st.columns(7)
            for j, letra in enumerate(abc[i:i+7]):
                l_min = letra.lower()
                with cols[j]:
                    if l_min in s["usadas"]:
                        st.markdown(f"<div style='text-align:center;'>{'✅' if l_min in s['palabra'] else '❌'}</div>", unsafe_allow_html=True)
                    else:
                        if st.button(letra, key=f"k-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()
        
        # 5. BOTÓN ARRIESGAR (Abajo a la derecha)
        st.write("---")
        c1, c2 = st.columns([0.6, 0.4])
        with c2:
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()

        if s["arriesgando"]:
            arr = st.text_input("¿Cuál es la palabra?", key="fa").lower().strip()
            if st.button("✔️ ENVIAR"):
                if arr == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()
        
        time.sleep(2)
        st.rerun()
