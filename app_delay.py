import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="AudioAlign Pro - Engenharia de Sistemas", layout="wide")

def calcular_v_som(t):
    return 331.3 + (0.606 * t)

# --- ESTILIZAÇÃO ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4b5062; }
    </style>
    """, unsafe_allow_html=True)

st.title("🔊 AudioAlign Pro: Calculadora de Delay")
st.markdown("### Ferramenta de Alinhamento Temporal para Engenheiros de Sistemas")

# --- BARRA LATERAL (INPUTS) ---
st.sidebar.header("⚙️ Parâmetros de Campo")

temp = st.sidebar.slider("Temperatura Ambiente (°C)", min_value=-10.0, max_value=50.0, value=25.0, step=0.5)
distancia_m = st.sidebar.number_input("Distância entre Fontes (Metros)", min_value=0.0, value=20.0, step=0.1)

st.sidebar.markdown("---")
st.sidebar.subheader("Ajustes de Processamento")
haas = st.sidebar.slider("Haas Offset (ms) - Localização Visual", 0.0, 20.0, 10.0, help="Adiciona um leve atraso para 'puxar' a imagem sonora para o palco.")
latencia_dsp = st.sidebar.number_input("Latência do Processador (ms)", value=0.0, step=0.1)

st.sidebar.markdown("---")
frequencia_alvo = st.sidebar.number_input("Frequência de Cruzamento (Hz)", value=100, step=10)

# --- CÁLCULOS TÉCNICOS ---
v_som = calcular_v_som(temp)
tempo_puro_ms = (distancia_m / v_som) * 1000
delay_final_ms = tempo_puro_ms + haas - latencia_dsp
distancia_virtual = (delay_final_ms / 1000) * v_som
comprimento_onda = v_som / frequencia_alvo if frequencia_alvo > 0 else 0

# --- EXIBIÇÃO DE RESULTADOS ---
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(label="VELOCIDADE DO SOM", value=f"{v_som:.2f} m/s")
    st.caption(f"Baseado em {temp}°C")

with col2:
    st.metric(label="TEMPO DE PROPAGAÇÃO", value=f"{tempo_puro_ms:.2f} ms")
    st.caption(f"Distância física pura: {distancia_m}m")

with col3:
    st.metric(label="VALOR NO PROCESSADOR", value=f"{delay_final_ms:.2f} ms", delta=f"{haas}ms Haas incl.")
    st.write("---")

# --- ÁREA DE ANÁLISE PROFISSIONAL ---
st.markdown("### 📊 Análise de Fase e Acústica")

tab1, tab2 = st.tabs(["Resumo Técnico", "Gráfico de Onda"])

with tab1:
    c1, c2 = st.columns(2)
    with c1:
        st.info(f"**Distância Acústica Virtual:** {distancia_virtual:.2f} metros")
        st.write("Isso é onde a caixa de delay 'parece' estar localizada em relação ao PA principal.")
    with c2:
        st.warning(f"**Comprimento de Onda em {frequencia_alvo}Hz:** {comprimento_onda:.2f} m")
        fase_relativa = (delay_final_ms % (1000/frequencia_alvo)) / (1000/frequencia_alvo) * 360
        st.write(f"**Desvio de Fase estimado:** {fase_relativa:.1f}°")

with tab2:
    st.write("Abaixo, uma visualização da diferença entre a distância física e o delay aplicado:")
    chart_data = pd.DataFrame({
        "Tipo": ["Físico (m)", "Virtual (m)"],
        "Metros": [distancia_m, distancia_virtual]
    })
    st.bar_chart(chart_data.set_index("Tipo"))

st.success(f"Dica do Engenheiro: Para {frequencia_alvo}Hz, um delay de {delay_final_ms:.2f}ms garante o alinhamento temporal. Verifique a fase com microfone RTA para ajuste fino final.")