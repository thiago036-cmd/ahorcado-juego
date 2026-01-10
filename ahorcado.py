import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Pro", layout="centered")

@st.cache_resource
def obtener_juego():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "tema": "oscuro", "arriesgando": False}

s = obtener_juego()
color_alerta = "#00ff88" if s["intentos"] >= 4 else "#ffcc00" if s["intentos"] >= 2 else "#ff4444"

# --- CSS MEJORADO: BOTONES CON BORDES FUERTES ---
st.markdown(f"""
    <style>
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; }}
    .stApp {{ background: #0f172a; color: white; }}

    /* MUÑECO BLINDADO */
    .muneco-box {{
        background: #1a1a1a;
        border: 3px solid {color_alerta};
        border-radius: 15px;
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

    /* PALABRA */
    .palabra-box {{
        font-size: 8vw !important;
        font-weight: bold;
        color: #fbbf24;
        text-align: center;
        margin: 10px 0;
    }}

    /* TECLADO CON BORDES GRUESOS Y BOTONES GRANDES */
    div[data-testid="stHorizontalBlock"] button {{
        height: 50px !important; /* Más alto para mejor toque */
        font-size: 18px !important; /* Letra más grande */
        font-weight: bold !important;
        border-radius: 10px !important;
        background: #1e293b !important;
        color: white !important;
        border: 3px solid #475569 !important; /* BORDE GRUESO */
        transition: 0.2s;
        margin-bottom: 5px;
    }}
    
    div[data-testid="stHorizontalBlock"] button:hover {{
        border-color: #38bdf8 !important;
        background: #334155 !important;
    }}

    /* BOTÓN ARRIESGAR */
    .stButton > button[key*="btn-arr"] {{
        background: #e67e22 !important;
        border: 3px solid #d35400 !important;
        height: 45px !important;
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

if not s["palabra"]:
    st.markdown("<h2 style='text-align:center;'>🎯 Nuevo Juego</h2>", unsafe_allow_html=True)
    p = st.text_input("Palabra Secreta:", type="password")
    if st.button("🚀 EMPEZAR", use_container_width=True):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado or s["intentos"] <= 0:
        if ganado: st.success("¡VICTORIA!")
        else: st.error(f"DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar, use_container_width=True)
    else:
        # 1. DIBUJO
        st.markdown(f'<div class="muneco-box"><div class="muneco-texto">{get_dibujo(s["intentos"])}</div></div>', unsafe_allow_html=True)

        # 2. VIDAS Y ARRIESGAR
        c_v, c_a = st.columns([0.4, 0.6])
        with c_v: st.markdown(f"<h3 style='margin:0;'>❤️ {s['intentos']}</h3>", unsafe_allow_html=True)
        with c_a: 
            if st.button("🔥 ARRIESGAR", key="btn-arr", use_container_width=True):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()

        if s["arriesgando"]:
            arr = st.text_input("Palabra completa:", key="fa").lower().strip()
            if st.button("ENVIAR", use_container_width=True):
                if arr == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()

        # 3. PALABRA
        v = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f'<div class="palabra-box">{v}</div>', unsafe_allow_html=True)

        # 4. TECLADO (Bordes reforzados)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            cols = st.columns(7)
            for j, letra in enumerate(abc[i:i+7]):
                l_min = letra.lower()
                with cols[j]:
                    if l_min in s["usadas"]:
                        st.markdown(f"<div style='text-align:center; font-size:20px;'>{'✅' if l_min in s['palabra'] else '❌'}</div>", unsafe_allow_html=True)
                    else:
                        if st.button(letra, key=f"k-{letra}"):
                            s["usadas"].append(l_min)
                            if l_min not in s["palabra"]: s["intentos"] -= 1
                            st.rerun()
        
        time.sleep(2)
        st.rerun()
