import streamlit as st
from streamlit_autorefresh import st_autorefresh
import streamlit.components.v1 as cp

st.set_page_config(page_title="Ahorcado MULTIJUGADOR", layout="centered")

# --- SINCRONIZACIÓN MULTIJUGADOR ---
# Leemos los datos directamente de la URL para que todos vean lo mismo
query = st.query_params
p_url = query.get("p", "") # Palabra secreta
u_url = query.get("u", "").split(",") if query.get("u") else [] # Letras usadas
v_url = int(query.get("v", 6)) # Vidas

# Refresco rápido para ver los movimientos del otro jugador
st_autorefresh(interval=1500, key="multi_sync")

st.markdown("""<style>
    .stApp { background:#0e1117; color:white; }
    [data-testid="stHorizontalBlock"] { display: grid !important; grid-template-columns: repeat(auto-fit, minmax(60px, 1fr)) !important; gap: 8px !important; justify-content: center !important; }
    button { background:#1c2128 !important; border: none !important; border-radius:8px !important; height:55px !important; min-width:60px !important; }
    button p { color:white !important; font-weight:800 !important; font-size:20px !important; margin:0 !important; }
    .w { font-size:35px; font-weight:900; letter-spacing:10px; text-align:center; color:#58a6ff; margin:20px 0; font-family:monospace; }
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

st.title("👥 AHORCADO COOPERATIVO")

if not p_url:
    txt = st.text_input("Palabra para tu hermano:", type="password")
    if st.button("🚀 CREAR PARTIDA", use_container_width=True):
        if txt: 
            st.query_params.update({"p": txt.lower().strip(), "u": "", "v": 6})
            st.rerun()
else:
    win = all(l in u_url or l==" " for l in p_url)
    if win or v_url <= 0:
        st.write("🏆 ¡GANARON!" if win else f"💀 PERDIERON. Era: {p_url.upper()}")
        if st.button("🔄 NUEVA PARTIDA", use_container_width=True):
            st.query_params.clear()
            st.rerun()
    else:
        draw(v_url)
        st.markdown(f"<div class='w'>{' '.join([l.upper() if l in u_url or l==' ' else '_' for l in p_url])}</div>", unsafe_allow_html=True)
        st.write(f"❤️ Vidas compartidas: {v_url}")
        abc = "ABCDEFGHIJKLMNÑOPQRSTUVWXYZ"
        cols = st.columns(len(abc))
        for i, l in enumerate(abc):
            with cols[i]:
                char = l.lower()
                if char in u_url:
                    st.button("✅" if char in p_url else "❌", key=f"b_{l}", disabled=True)
                elif st.button(l, key=f"b_{l}"):
                    u_url.append(char)
                    new_v = v_url - 1 if char not in p_url else v_url
                    st.query_params.update({"u": ",".join(u_url), "v": new_v})
                    st.rerun()
