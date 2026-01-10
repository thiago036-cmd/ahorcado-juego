import streamlit as st
import time

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado Pro", layout="centered")

@st.cache_resource
def obtener_juego():
    return {"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "tema": "oscuro", "arriesgando": False}

s = obtener_juego()
color_muneco = "#00ff88" if s["intentos"] >= 4 else "#ffcc00" if s["intentos"] >= 2 else "#ff4444"

# --- CSS ULTRA COMPACTO Y FIJADOR DE MUÑECO ---
st.markdown(f"""
    <style>
    /* Eliminar espacios vacíos de Streamlit */
    .block-container {{ padding-top: 1rem !important; padding-bottom: 0rem !important; }}
    div[data-testid="stVerticalBlock"] {{ gap: 0.5rem !important; }}
    
    .stApp {{ background: #0f172a; color: white; }}

    /* MUÑECO BLINDADO: NO SE MUEVE NI SE DESARMA */
    .muneco-box {{
        background: #1e293b;
        border: 2px solid {color_muneco};
        border-radius: 15px;
        padding: 10px;
        display: block;
        width: fit-content;
        margin: 0 auto;
        line-height: 1 !important;
    }}
    .muneco-texto {{
        font-family: 'Courier New', monospace !important;
        font-size: 14px !important;
        color: {color_muneco} !important;
        white-space: pre !important; /* Mantiene la forma */
        margin: 0 !important;
        display: inline-block;
        text-align: left;
    }}

    /* PALABRA COMPACTA */
    .palabra-box {{
        font-size: 7vw !important;
        font-weight: 800;
        color: #fbbf24;
        text-align: center;
        letter-spacing: 3px;
        margin: 10px 0;
    }}

    /* TECLADO PEQUEÑO PARA QUE QUEPA TODO */
    div[data-testid="stHorizontalBlock"] button {{
        height: 35px !important;
        padding: 0 !important;
        font-size: 14px !important;
        border-radius: 5px !important;
        background: #334155 !important;
        color: white !important;
        border: 1px solid #475569 !important;
    }}

    /* BOTÓN ARRIESGAR */
    .stButton > button[key*="btn-arr"] {{
        background: #e67e22 !important;
        height: 40px !important;
    }}
    </style>
    """, unsafe_allow_html=True)

def reiniciar():
    s.update({"palabra": "", "usadas": [], "intentos": 6, "gano_directo": False, "arriesgando": False})
    st.rerun()

def get_dibujo(i):
    # Dibujo simplificado para máxima estabilidad
    etapas = [
        "  +---+\n  |   |\n  O   |\n /|\\  |\n / \\  |\n      |\n=========", #0
        "  +---+\n  |   |\n  O   |\n /|\\  |\n /    |\n      |\n=========", #1
        "  +---+\n  |   |\n  O   |\n /|\\  |\n      |\n      |\n=========", #2
        "  +---+\n  |   |\n  O   |\n /|   |\n      |\n      |\n=========", #3
        "  +---+\n  |   |\n  O   |\n  |   |\n      |\n      |\n=========", #4
        "  +---+\n  |   |\n  O   |\n      |\n      |\n      |\n=========", #5
        "  +---+\n  |   |\n      |\n      |\n      |\n      |\n========="  #6
    ]
    return etapas[i]

if not s["palabra"]:
    st.title("🏹 Ahorcado")
    p = st.text_input("Palabra:", type="password")
    if st.button("JUGAR"):
        if p:
            s.update({"palabra": p.lower().strip(), "usadas": [], "intentos": 6})
            st.rerun()
else:
    ganado = all(l in s["usadas"] or l == " " for l in s["palabra"]) or s["gano_directo"]
    
    if ganado or s["intentos"] <= 0:
        if ganado: st.success("¡GANASTE!")
        else: st.error(f"PERDISTE: {s['palabra'].upper()}")
        st.button("OTRA VEZ", on_click=reiniciar)
    else:
        # 1. MUÑECO (Usando div para control total)
        st.markdown(f'<div class="muneco-box"><div class="muneco-texto">{get_dibujo(s["intentos"])}</div></div>', unsafe_allow_html=True)

        # 2. VIDAS Y ARRIESGAR EN UNA FILA
        c_v, c_a = st.columns([0.5, 0.5])
        with c_v: st.markdown(f"❤️ **{s['intentos']}**")
        with c_a: 
            if st.button("🔥 ARRIESGAR", key="btn-arr"):
                s["arriesgando"] = not s["arriesgando"]
                st.rerun()

        if s["arriesgando"]:
            arr = st.text_input("Palabra:", key="fa").lower().strip()
            if st.button("OK"):
                if arr == s["palabra"]: s["gano_directo"] = True
                else: s["intentos"] = 0
                st.rerun()

        # 3. PALABRA
        v = " ".join([l.upper() if l in s["usadas"] or l == " " else "_" for l in s["palabra"]])
        st.markdown(f'<div class="palabra-box">{v}</div>', unsafe_allow_html=True)

        # 4. TECLADO COMPACTO
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        for i in range(0, len(abc), 7):
            cols = st.columns(7)
            for j, letra in enumerate(abc[i:i+7]):
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
