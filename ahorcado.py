import streamlit as st
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Ahorcado Co-op", layout="centered")

# --- MOTOR DE SESIÓN GLOBAL ---
# Usamos cache_resource para que todos los que entren vean la misma variable 's'
@st.cache_resource
def obtener_estado_global():
    return {
        "palabra": "", 
        "usadas": [], 
        "intentos": 6, 
        "gano_directo": False,
        "arriesgando": False,
        "ultima_act": time.time()
    }

s = obtener_estado_global()

# --- CSS: TECLADO FLEXIBLE Y DISEÑO VERTICAL ---
color_alerta = "#00ff88" if s["intentos"] >= 4 else "#ffcc00" if s["intentos"] >= 2 else "#ff4444"

st.markdown(f"""
    <style>
    .stApp {{ background: #0f172a; color: white; }}
    
    /* MUÑECO VERTICAL Y CENTRADO */
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

    /* PALABRA SEGUIDA DE LAS VIDAS */
    .palabra-box {{
        font-size: 8vw !important;
        font-weight: 900;
        color: #fbbf24;
        text-align: center;
        margin: 10px 0;
    }}

    /* TECLADO MÓVIL: Evita que las letras se pongan verticales */
    .stHorizontalBlock {{
        display: flex !important;
        flex-wrap: wrap !important; /* Permite que bajen a la siguiente fila si no caben */
        justify-content: center !important;
        gap: 5px !important;
    }}
    
    div[data-testid="stHorizontalBlock"] > div {{
        flex: 1 1 12% !important; /* Fuerza un ancho mínimo para que entren 7 u 8 por fila */
        min-width: 40px !important;
    }}

    .stButton > button {{
        width: 100% !important;
        height: 45px !important;
        padding: 0 !important;
        font-weight: bold !important;
        border: 2px solid #475569 !important;
        border-radius: 8px !important;
    }}

    /* BOTÓN ARRIESGAR ABAJO A LA DERECHA */
    .btn-arriesgar-container {{
        display: flex;
        justify-content: flex-end;
        margin-top: 20px;
    }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False, "ultima_act": time.time()})
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

# --- LÓGICA DE UNIÓN AUTOMÁTICA ---
# Esto hace que la página se refresque sola cada 3 segundos para ver cambios de otros
if s["palabra"]:
    st.empty() # Placeholder
    # Solo refrescamos si no hemos ganado ni perdido
    ganado_check = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    if not ganado_check and s["intentos"] > 0:
        time.sleep(3)
        st.rerun()

# --- INTERFAZ ---
if not s["palabra"]:
    st.title("🎯 Nueva Sesión")
    p = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 CREAR PARA TODOS"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6, "ultima_act": time.time()})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado or s["intentos"] <= 0:
        if ganado: st.success("¡VICTORIA COLECTIVA!")
        else: st.error(f"GAME OVER. ERA: {s['palabra'].upper()}")
        st.button("🔄 NUEVA PARTIDA", on_click=reiniciar)
    else:
        # 1. DIBUJO
        st.markdown(f'<div class="muneco-box"><div class="muneco-texto">{get_dibujo(s["intentos"])}</div></div>', unsafe_allow_html=True)

        # 2. VIDAS
        st.markdown(f"<div style='text-align:center;'>❤️ <b>{s['intentos']}</b> VIDAS</div>", unsafe_allow_html=True)

        # 3. PALABRA
        visual = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f'<div class="palabra-box">{visual}</div>', unsafe_allow_html=True)

        # 4. TECLADO (Flexbox para evitar verticalidad)
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(7) # Streamlit intentará poner 7, el CSS forzará el comportamiento
        for i, letra in enumerate(abc):
            l_min = letra.lower()
            with cols[i % 7]:
                if l_min in s["usadas"]:
                    st.markdown(f"<div style='text-align:center; height:45px;'>{'✅' if l_min in s['palabra'] else '❌'}</div>", unsafe_allow_html=True)
                else:
                    if st.button(letra, key=f"k-{letra}"):
                        s["usadas"].append(l_min)
                        if l_min not in s["palabra"]: s["intentos"] -= 1
                        s["ultima_act"] = time.time()
                        st.rerun()

        # 5. BOTÓN ARRIESGAR (Abajo a la derecha)
        st.markdown('<div class="btn-arriesgar-container">', unsafe_allow_html=True)
        col_espacio, col_btn = st.columns([0.6, 0.4])
        with col_btn:
            if st.button("🔥 ARRIESGAR", key="btn-arr"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()
        st.markdown('</div>', unsafe_allow_html=True)

        if s["arriesgando"]:
            arr = st.text_input("Palabra completa:", key="fa").lower().strip()
            if st.button("✔️ ENVIAR"):
                if arr == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                s["ultima_act"] = time.time()
                st.rerun()
