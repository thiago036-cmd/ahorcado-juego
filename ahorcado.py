import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as cp

# --- CONFIGURACIÓN Y ESTADO ---
st.set_page_config(page_title="Ahorcado", layout="wide")
if "p" not in st.session_state: 
    st.session_state.update({"p":"","u":[],"v":6}) # p: palabra, u: letras usadas, v: vidas
st_autorefresh(interval=2000, key="sync") # Refresco automático para sincronizar estados

# --- DISEÑO VISUAL (CSS) ---
st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    /* Ajuste del teclado: crea una rejilla adaptable */
    [data-testid="stHorizontalBlock"] { 
        display: grid !important; 
        grid-template-columns: repeat(auto-fit, minmax(80px, 1fr)) !important; 
        gap: 10px !important; 
    }
    /* En celulares (pantalla < 600px) muestra 4 botones por fila */
    @media (max-width: 600px) { [data-testid="stHorizontalBlock"] { grid-template-columns: repeat(4, 1fr) !important; } }
    
    /* Estilo de los botones (Teclas) */
    button { 
        background:#1c2128 !important; border: none !important; border-radius: 8px !important; 
        height:60px !important; width:1000% !important;
        display: flex !important; align-items: center !important; justify-content: center !important;
        padding: 0 !important; 
    }
    /* Estilo del texto dentro del botón (Centrado perfecto) */
    button p { 
        color:white !important; font-weight:700 !important; font-size:24px !important; 
        margin:0 !important; line-height: 1 !important;
    }
    button:hover { background:#30363d !important; } /* Cambio de color al pasar el mouse */
    .w { font-size:40px; font-weight:900; letter-spacing:12px; text-align:center; color:#58a6ff; margin:20px 0; }
</style>""", unsafe_allow_html=True)

# --- FUNCIÓN PARA DIBUJAR EL AHORCADO (SVG) ---
def draw(v):
    c, p = "#7cfc00", lambda cond, d: d if cond else ""
    svg = f"""<div style="display:flex;justify-content:center;background:#11151c;border-radius:15px;height:170px;">
    <svg width="150" height="150" viewBox="0 0 200 200">
        <path d="M20 180 H100 M60 180 V20 H140 V50" stroke="white" stroke-width="6" fill="none"/>
        {p(v<=5, f'<circle cx="140" cy="65" r="15" stroke="{c}" stroke-width="4" fill="none"/>')} # Cabeza
        {p(v<=4, f'<line x1="140" y1="80" x2="140" y2="130" stroke="{c}" stroke-width="4"/>')}    # Cuerpo
        {p(v<=3, f'<line x1="140" y1="95" x2="115" y2="115" stroke="{c}" stroke-width="4"/>')}   # Brazo Izq
        {p(v<=2, f'<line x1="140" y1="95" x2="165" y2="115" stroke="{c}" stroke-width="4"/>')}   # Brazo Der
        {p(v<=1, f'<line x1="140" y1="130" x2="115" y2="160" stroke="{c}" stroke-width="4"/>')}  # Pierna Izq
        {p(v<=0, f'<line x1="140" y1="130" x2="165" y2="160" stroke="{c}" stroke-width="4"/>')}  # Pierna Der
    </svg></div>"""
    cp.html(svg, height=180)

# --- LÓGICA DEL JUEGO ---
st.title("🕹️ AHORCADO")
s = st.session_state
if not s.p: # Si no hay palabra definida, pedirla
    txt = st.text_input("ESCRIBE LA PALABRA:", type="password")
    if st.button("INICIAR"): s.p, s.u, s.v = txt.lower().strip(), [], 6; st.rerun()
else:
    win = all(l in s.u or l==" " for l in s.p) # Verifica si todas las letras están en 'usadas'
    if win or s.v <= 0: # Pantalla de fin de juego
        st.write("🏆 GANASTE" if win else f"💀 PALABRA: {s.p.upper()}")
        if st.button("REINTENTAR"): s.p = ""; st.rerun()
    else:
        draw(s.v) # Dibujar monigote
        # Mostrar guiones bajos o letras acertadas
        st.markdown(f"<div class='w'>{' '.join([l.upper() if l in s.u or l==' ' else '_' for l in s.p])}</div>", unsafe_allow_html=True)
        st.write(f"❤️ Vidas restantes: {s.v}")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(abc)) # Crea columnas para el teclado
        for i, l in enumerate(abc):
            with cols[i]:
                if l.lower() in s.u: # Si la letra ya se pulsó, deshabilitar botón
                    st.button("✅" if l.lower() in s.p else "❌", key=l, disabled=True)
                elif st.button(l, key=l): # Lógica al pulsar una letra nueva
                    s.u.append(l.lower())
                    if l.lower() not in s.p: s.v -= 1 # Restar vida si falla
                    st.rerun()





