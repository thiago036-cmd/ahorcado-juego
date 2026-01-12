import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as cp

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado GLOBAL", layout="centered")
st_autorefresh(interval=1500, key="global_sync")

# --- MEMORIA COMPARTIDA (SERVIDOR) ---
@st.cache_resource
def get_global_state():
    return {"p": "", "u": [], "v": 6}

state = get_global_state()

# --- DISEÑO VISUAL (CSS) ---
st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    
    /* Contenedor de teclado con botones grandes */
    [data-testid="stHorizontalBlock"] { 
        display: grid !important; 
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)) !important; 
        gap: 12px !important; 
        justify-content: center !important;
    }
    
    /* Botones de letras grandes y centrados */
    button { 
        background:#1c2128 !important; border: none !important; border-radius:10px !important; 
        height:70px !important; min-width:80px !important;
        display: flex !important; align-items: center !important; justify-content: center !important; 
        padding: 0 !important;
    }
    button p { color:white !important; font-weight:900 !important; font-size:28px !important; margin:0 !important; line-height: 1 !important; }
    
    /* Estilo para el botón de Arriesgar */
    .stButton > button[kind="secondary"] { background: #e91e63 !important; height: 45px !important; min-width: 100% !important; }
    .stButton > button[kind="secondary"] p { font-size: 18px !important; }

    .w { font-size:40px; font-weight:900; letter-spacing:12px; text-align:center; color:#58a6ff; margin:25px 0; font-family:monospace; }
</style>""", unsafe_allow_html=True)

def draw(v):
    c, p = "#7cfc00", lambda cond, d: d if cond else ""
    svg = f"""<div style="display:flex;justify-content:center;background:#11151c;border-radius:15px;height:160px;">
    <svg width="140" height="140" viewBox="0 0 200 200"><path d="M20 180 H100 M60 180 V20 H140 V50" stroke="white" stroke-width="6" fill="none"/>
        {p(v<=5, f'<circle cx="140" cy="65" r="15" stroke="{c}" stroke-width="4" fill="none"/>')}
        {p(v<=4, f'<line x1="140" y1="80" x2="140" y2="130" stroke="{c}" stroke-width="4"/>')}
        {p(v<=3, f'<line x1="140" y1="95" x2="115" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=2, f'<line x1="140" y1="95" x2="165" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=1, f'<line x1="140" y1="130" x2="115" y2="160" stroke="{c}" stroke-width="4"/>')}
        {p(v<=0, f'<line x1="140" y1="130" x2="165" y2="160" stroke="{c}" stroke-width="4"/>')}
    </svg></div>"""
    cp.html(svg, height=170)

st.title("🌎 AHORCADO GLOBAL")

if not state["p"]:
    txt = st.text_input("Palabra secreta para la sala:", type="password")
    if st.button("🚀 INICIAR PARTIDA", use_container_width=True):
        if txt: state["p"]=txt.lower().strip(); state["u"]=[]; state["v"]=6; st.rerun()
else:
    win = all(l in state["u"] or l==" " for l in state["p"])
    if win or state["v"] <= 0:
        st.write("🏆 ¡VICTORIA COLECTIVA!" if win else f"💀 PERDIMOS. La palabra era: {state['p'].upper()}")
        if st.button("🔄 REINICIAR SERVIDOR", use_container_width=True): state["p"]=""; st.rerun()
    else:
        draw(state["v"])
        
        # --- SECCIÓN DE ARRIESGAR ---
        with st.expander("🔥 ARRIESGAR TODO"):
            intento = st.text_input("Escribe la palabra completa:", placeholder="Cuidado: si fallas, pierdes.")
            if st.button("CONFIRMAR ARRIESGAR"):
                if intento.lower().strip() == state["p"]:
                    state["u"] = list(state["p"]) # Desbloquea todas las letras
                else:
                    state["v"] = 0 # Mata al personaje
                st.rerun()

        st.markdown(f"<div class='w'>{' '.join([l.upper() if l in state['u'] or l==' ' else '_' for l in state['p']])}</div>", unsafe_allow_html=True)
        st.write(f"❤️ Vidas del servidor: {state['v']}")
        
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(abc))
        for i, l in enumerate(abc):
            with cols[i]:
                char = l.lower()
                if char in state["u"]:
                    st.button("✅" if char in state["p"] else "❌", key=f"g_{l}", disabled=True)
                elif st.button(l, key=f"g_{l}"):
                    state["u"].append(char)
                    if char not in state["p"]: state["v"] -= 1
                    st.rerun()
