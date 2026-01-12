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

# --- DISEÑO VISUAL DEFINITIVO ---
st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    
    /* TECLADO CON ESPACIADO DE 60PX REAL */
    [data-testid="stHorizontalBlock"] { 
        gap: 60px !important; 
        justify-content: center !important; 
        display: flex !important; 
        flex-wrap: wrap !important; 
    }

    /* BOTONES CHIQUITOS (50x50) */
    button, .stButton>button { 
        background-color: #1c2128 !important; 
        border: none !important; 
        border-radius: 8px !important; 
        height: 50px !important; 
        width: 50px !important; 
        min-width: 50px !important;
        padding: 0 !important;
        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
    }
    
    /* EVITAR QUE LAS LETRAS SE VEAN UNA DEBAJO DE OTRA */
    button p, .stButton>button p { 
        font-size: 20px !important; 
        font-weight: 800 !important; 
        color: white !important;
        white-space: nowrap !important; /* Prohibe el salto de línea */
        overflow: visible !important;
        margin: 0 !important;
    }

    /* CONTADOR DE VIDAS TIPO BANNER */
    .vidas-banner {
        text-align: center;
        background: rgba(255, 75, 75, 0.1);
        border: 1px solid #ff4b4b;
        padding: 12px;
        border-radius: 12px;
        font-size: 22px;
        margin-bottom: 15px;
        color: #ff4b4b;
    }

    .w { font-size:35px; font-weight:900; letter-spacing:12px; text-align:center; color:#58a6ff; margin:20px 0; font-family:monospace; }
</style>""", unsafe_allow_html=True)

def draw(v):
    c, p = "#7cfc00", lambda cond, d: d if cond else ""
    svg = f"""<div style="display:flex;justify-content:center;background:#11151c;border-radius:15px;height:140px;">
    <svg width="120" height="120" viewBox="0 0 200 200"><path d="M20 180 H100 M60 180 V20 H140 V50" stroke="white" stroke-width="6" fill="none"/>
        {p(v<=5, f'<circle cx="140" cy="65" r="15" stroke="{c}" stroke-width="4" fill="none"/>')}
        {p(v<=4, f'<line x1="140" y1="80" x2="140" y2="130" stroke="{c}" stroke-width="4"/>')}
        {p(v<=3, f'<line x1="140" y1="95" x2="115" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=2, f'<line x1="140" y1="95" x2="165" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=1, f'<line x1="140" y1="130" x2="115" y2="160" stroke="{c}" stroke-width="4"/>')}
        {p(v<=0, f'<line x1="140" y1="130" x2="165" y2="160" stroke="{c}" stroke-width="4"/>')}
    </svg></div>"""
    cp.html(svg, height=150)

st.title("🌎 AHORCADO GLOBAL")

if not state["p"]:
    txt = st.text_input("Palabra secreta:", type="password")
    if st.button("🚀 INICIAR PARTIDA"):
        if txt: 
            state["p"] = txt.lower().strip()
            state["u"] = []
            state["v"] = 6
            st.rerun()
else:
    win = all(l in state["u"] or l==" " for l in state["p"])
    if win or state["v"] <= 0:
        st.write("🏆 ¡VICTORIA!" if win else f"💀 LA PALABRA ERA: {state['p'].upper()}")
        if st.button("🔄 REINICIAR"):
            state["p"] = ""
            st.rerun()
    else:
        # CONTADOR DE VIDAS CON CORAZONES
        coras = "❤️" * state["v"]
        st.markdown(f'<div class="vidas-banner">{coras}<br>Vidas restantes: {state["v"]}</div>', unsafe_allow_html=True)
        
        draw(state["v"])
        
        with st.expander("🔥 ARRIESGAR"):
            intento = st.text_input("Escribe la palabra:", key="risk")
            if st.button("CONFIRMAR ARRIESGAR"):
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
