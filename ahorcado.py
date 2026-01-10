import streamlit as st

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Ahorcado Realtime Pro", layout="centered")

# --- MOTOR DE SESIÓN GLOBAL ---
@st.cache_resource
def obtener_estado_global():
    return {
        "palabra": "", 
        "usadas": [], 
        "intentos": 6, 
        "gano_directo": False,
        "arriesgando": False
    }

s = obtener_estado_global()

# --- AUTO-REFRESH (JS) ---
# Este bloque hace que la página se refresque sola cada 2 segundos
st.components.v1.html(
    """
    <script>
    window.parent.document.dispatchEvent(new CustomEvent("st:refresh"));
    setTimeout(function() {
        window.parent.location.reload();
    }, 2000); 
    </script>
    """,
    height=0,
)

# --- DISEÑO CSS ---
color_alerta = "#00ff88" if s["intentos"] >= 4 else "#ffcc00" if s["intentos"] >= 2 else "#ff4444"

st.markdown(f"""
    <style>
    .stApp {{ background: #0f172a; color: white; }}
    
    .muneco-box {{
        background: #1a1a1a;
        border: 3px solid {color_alerta};
        border-radius: 20px;
        padding: 10px;
        width: 140px;
        margin: 0 auto 10px auto;
        text-align: center;
    }}
    .muneco-texto {{
        font-family: 'Courier New', monospace !important;
        font-size: 16px !important;
        color: {color_alerta} !important;
        white-space: pre !important;
        line-height: 1.1 !important;
        display: inline-block;
        text-align: left;
    }}

    .palabra-box {{
        font-size: 8vw !important;
        font-weight: 900;
        color: #fbbf24;
        text-align: center;
        margin: 10px 0;
    }}

    /* Teclado que no se rompe en móvil */
    div[data-testid="stHorizontalBlock"] {{
        display: flex !important;
        flex-wrap: wrap !important;
        justify-content: center !important;
        gap: 4px !important;
    }}
    
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 12% !important;
        min-width: 42px !important;
    }}

    .stButton > button {{
        width: 100% !important;
        height: 45px !important;
        font-weight: bold !important;
        border: 2px solid #475569 !important;
        border-radius: 8px !important;
    }}

    .stButton > button[key*="btn-arr"] {{
        background: #e67e22 !important;
        border: 2px solid white !important;
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
    st.title("🎯 Ahorcado Co-op")
    palabra_input = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 INICIAR"):
        if palabra_input:
            s["palabra"] = palabra_input.lower().strip()
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    perdido = s["intentos"] <= 0

    if ganado:
        st.balloons()
        st.success(f"🏆 ¡VICTORIA! ERA: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar)
    elif perdido:
        st.error(f"💀 DERROTA. ERA: {s['palabra'].upper()}")
        st.button("🔄 REINTENTAR", on_click=reiniciar)
    else:
        # 1. DIBUJO
        st.markdown(f'<div class="muneco-box"><div class="muneco-texto">{get_dibujo(s["intentos"])}</div></div>', unsafe_allow_html=True)

        # 2. VIDAS
        st.markdown(f"<div style='text-align:center;'>❤️ <b>{s['intentos']}</b> VIDAS</div>", unsafe_allow_html=True)

        # 3. PALABRA
        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f'<div class="palabra-box">{visual}</div>', unsafe_allow_html=True)

        # 4. TECLADO
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7)
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["usadas"]:
                    color_txt = "#00ff88" if l_min in s["palabra"] else "#ff4444"
                    st.markdown(f"<div style='text-align:center; color:{color_txt}; font-weight:bold; height:45px; line-height:45px;'>{letra}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"k-{letra}"):
                        s["usadas"].append(l_min)
                        if l_min not in s["palabra"]: s["intentos"] -= 1
                        st.rerun()

        # 5. ARRIESGAR (Abajo a la derecha)
        st.write("---")
        c_esp, c_arr = st.columns([0.6, 0.4])
        with c_arr:
            if st.button("🔥 ARRIESGAR", key="btn-arr"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()

        if s["arriesgando"]:
            arr = st.text_input("¿Qué palabra es?", key="fa").lower().strip()
            if st.button("✔️ ENVIAR"):
                if arr == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()
