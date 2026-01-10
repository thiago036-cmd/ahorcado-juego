import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as cp

# --- CONFIGURACIÓN ---
st.set_page_config(page_title="Ahorcado", layout="wide")
if "p" not in st.session_state: 
    st.session_state.update({"p":"","u":[],"v":6})
st_autorefresh(interval=2000, key="sync")

# --- DISEÑO VISUAL (CSS) ---
st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    /* Estilo para el input de texto y botones de control */
    .stTextInput input { background:#1c2128 !important; color:white !important; border:1px solid #30363d !important; border-radius:8px !important; }
    
    /* Grid del teclado */
    [data-testid="stHorizontalBlock"] { 
        display: grid !important; 
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)) !important; 
        gap: 10px !important; 
    }
    @media (max-width: 600px) { [data-testid="stHorizontalBlock"] { grid-template-columns: repeat(4, 1fr) !important; } }
    
    /* Botones de letras (Sin bordes y centrados) */
    button { 
        background:#1c2128 !important; border: none !important; border-radius:8px !important; 
        height:60px !important; width:70% !important;
        display: flex !important; align-items: center !important; justify-content: center !important; padding: 0 !important; 
    }
    button p { color:white !important; font-weight:700 !important; font-size:24px !important; margin:0 !important; line-height: 1 !important; }
    button:hover { background:#30363d !important; }
    .w { font-size:45px; font-weight:900; letter-spacing:15px; text-align:center; color:#58a6ff; margin:25px 0; font-family: monospace; }
</style>""", unsafe_allow_html=True)

# --- DIBUJO SVG ---
def draw(v):
    c, p = "#7cfc00", lambda cond, d: d if cond else ""
    svg = f"""<div style="display:flex;justify-content:center;background:#11151c;border-radius:15px;height:170px;">
    <svg width="150" height="150" viewBox="0 0 200 200">
        <path d="M20 180 H100 M60 180 V20 H140 V50" stroke="white" stroke-width="6" fill="none"/>
        {p(v<=5, f'<circle cx="140" cy="65" r="15" stroke="{c}" stroke-width="4" fill="none"/>')}
        {p(v<=4, f'<line x1="140" y1="80" x2="140" y2="130" stroke="{c}" stroke-width="4"/>')}
        {p(v<=3, f'<line x1="140" y1="95" x2="115" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=2, f'<line x1="140" y1="95" x2="165" y2="115" stroke="{c}" stroke-width="4"/>')}
        {p(v<=1, f'<line x1="140" y1="130" x2="115" y2="160" stroke="{c}" stroke-width="4"/>')}
        {p(v<=0, f'<line x1="140" y1="130" x2="165" y2="160" stroke="{c}" stroke-width="4"/>')}
    </svg></div>"""
    cp.html(svg, height=180)

# --- FLUJO DEL JUEGO ---
st.title("🕹️ AHORCADO")
s = st.session_state
if not s.p:
    # Contenedor para centrar el formulario de inicio
    with st.container():
        st.subheader("Configuración inicial")
        txt = st.text_input("Ingresa la frase o palabra secreta:", type="password", placeholder="Escribe aquí...")
        if st.button("🚀 EMPEZAR JUEGO", use_container_width=True): # Botón ancho para iniciar
            if txt: s.p, s.u, s.v = txt.lower().strip(), [], 6; st.rerun()
else:
    win = all(l in s.u or l==" " for l in s.p)
    if win or s.v <= 0:
        st.write("🏆 ¡VICTORIA!" if win else f"💀 FIN DEL JUEGO. La palabra era: {s.p.upper()}")
        if st.button("🔄 JUGAR OTRA VEZ", use_container_width=True): s.p = ""; st.rerun()
    else:
        draw(s.v)
        st.markdown(f"<div class='w'>{' '.join([l.upper() if l in s.u or l==' ' else '_' for l in s.p])}</div>", unsafe_allow_html=True)
        st.write(f"❤️ Vidas: {s.v} de 6")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(abc))
        for i, l in enumerate(abc):
            with cols[i]:
                if l.lower() in s.u: st.button("✅" if l.lower() in s.p else "❌", key=l, disabled=True)
                elif st.button(l, key=l):
                    s.u.append(l.lower()); s.v -= 1 if l.lower() not in s.p else 0; st.rerun()


