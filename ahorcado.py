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

# --- DISEÑO VISUAL CORREGIDO ---
st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    
    /* Contenedor de teclado: asegura que las columnas no aprieten los botones */
    [data-testid="stHorizontalBlock"] { 
        display: grid !important; 
        grid-template-columns: repeat(auto-fit, minmax(85px, 1fr)) !important; 
        gap: 12px !important; 
        justify-content: center !important;
    }
    [data-testid="column"] { width: auto !important; flex: none !important; }

    /* FORZAR ESTILO EN TODOS LOS BOTONES (QUITAR ROSA Y FLACURA) */
    button, .stButton>button { 
        background-color: #1c2128 !important; 
        color: white !important;
        border: none !important; 
        border-radius: 10px !important; 
        height: 75px !important; 
        width: 100% !important;
        min-width: 85px !important;
        display: flex !important; 
        align-items: center !important; 
        justify-content: center !important; 
        padding: 0 !important;
    }

    /* Color de hover para que se note el click */
    button:hover { background-color: #30363d !important; border: none !important; }

    /* Letras grandes, blancas y centradas */
    button p, .stButton>button p { 
        color: white !important; 
        font-weight: 900 !important; 
        font-size: 30px !important; 
        margin: 0 !important; 
        line-height: 1 !important;
    }
    
    /* Botón de Arriesgar (lo mantenemos diferente pero no rosa) */
    .stExpander button { background: #238636 !important; height: 50px !important; }
    .stExpander button p { font-size: 20px !important; }

    .w { font-size:45px; font-weight:900; letter-spacing:15px; text-align:center; color:#58a6ff; margin:25px 0; font-family:monospace; }
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
    txt = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 INICIAR PARTIDA"):
        if txt: state["p"]=txt.lower().strip(); state["u"]=[]; state["v"]=6; st.rerun()
else:
    win = all(l in state["u"] or l==" " for l in state["p"])
    if win or state["v"] <= 0:
        st.write("🏆 ¡VICTORIA!" if win else f"💀 PERDIMOS: {state['p'].upper()}")
        if st.button("🔄 REINICIAR"): state["p"]=""; st.rerun()
    else:
        draw(state["v"])
        with st.expander("🔥 ARRIESGAR TODO"):
            intento = st.text_input("Palabra completa:", key="arriesgar_input")
            if st.button("CONFIRMAR"):
                if intento.lower().strip() == state["p"]: state["u"] = list(state["p"])
                else: state["v"] = 0
                st.rerun()

        st.markdown(f"<div class='w'>{' '.join([l.upper() if l in state['u'] or l==' ' else '_' for l in state['p']])}</div>", unsafe_allow_html=True)
        
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(abc))
        for i, l in enumerate(abc):
            with cols[i]:
                char = l.lower()
                if char in state["u"]:
                    st.button("✅" if char in state["p"] else "❌", key=f"btn_{l}", disabled=True)
                elif st.button(l, key=f"btn_{l}"):
                    state["u"].append(char)
                    if char not in state["p"]: state["v"] -= 1
                    st.rerun()
