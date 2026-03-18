import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="AudioAlign Pro - Precisão", page_icon="🔊", layout="wide")

def calcular_v_som(t):
    # Fórmula padrão da engenharia acústica: v = 331.3 + 0.606 * T
    return 331.3 + (0.606 * t)

st.title("🔊 AudioAlign Multi-Tower Pro")
st.markdown("### Sistema de Alinhamento Temporal de Alta Precisão")

# --- BARRA LATERAL: CONTROLES GLOBAIS ---
st.sidebar.header("⚙️ Parâmetros de Sistema")

# 1. Temperatura
temp = st.sidebar.number_input("Temperatura Ambiente (°C)", value=25.0, step=0.1, help="Afeta diretamente a velocidade do som.")
v_som = calcular_v_som(temp)
st.sidebar.caption(f"Velocidade do Som: {v_som:.2f} m/s")

st.sidebar.markdown("---")

# 2. Haas Global (Agora com Input Numérico de precisão)
st.sidebar.subheader("🎯 Ajuste de Haas (Precedence)")
haas_global = st.sidebar.number_input(
    "Haas Global (ms)", 
    min_value=0.0, 
    max_value=30.0, 
    value=7.0, 
    step=0.1,
    help="Tempo adicional para garantir que a localização sonora venha do palco. Sugerido: 5ms a 15ms."
)

# 3. Latência de DSP
latencia_dsp = st.sidebar.number_input(
    "Latência Interna DSP (ms)", 
    min_value=0.0, 
    value=0.0, 
    step=0.01,
    help="Latência fixa do processador/amplificador (ver no manual do fabricante)."
)

# --- CONFIGURAÇÃO DAS TORRES NO PAINEL PRINCIPAL ---
st.markdown("---")
num_torres = st.number_input("Quantidade de Torres de Delay", min_value=1, max_value=20, value=2)

st.info(f"💡 Dica de Engenharia: Com {temp}°C, o som percorre 1 metro a cada {1000/v_som:.3f} ms.")

dados_torres = []

# Layout de entrada por torre
for i in range(int(num_torres)):
    with st.expander(f"📍 Configuração: Torre {i+1}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 2])
        
        with col1:
            nome = st.text_input(f"Identificação", value=f"Torre {i+1}", key=f"nome_{i}")
        with col2:
            distancia = st.number_input(f"Distância do Palco (Metros)", min_value=0.0, value=20.0 + (i*15), step=0.01, key=f"dist_{i}")
        with col3:
            # O Haas individual herda o valor global do sidebar, mas permite override
            haas_individual = st.number_input(f"Haas da Torre (ms)", value=haas_global, step=0.1, key=f"haas_{i}")

        # Cálculos Matemáticos
        tempo_propagacao = (distancia / v_som) * 1000
        # Fórmula: Delay = (Dist/V) + Haas - Latência
        delay_total = tempo_propagacao + haas_individual - latencia_dsp
        distancia_virtual = (delay_total / 1000) * v_som
        
        dados_torres.append({
            "Torre": nome,
            "Distância Real (m)": distancia,
            "Tempo Puro (ms)": round(tempo_propagacao, 3),
            "Haas Aplicado (ms)": haas_individual,
            "VALOR DSP (ms)": round(delay_total, 2),
            "Dist. Virtual (m)": round(distancia_virtual, 2)
        })

# --- TABELA DE RESULTADOS ---
st.markdown("---")
st.subheader("📋 Mapa de Delay para o Técnico de Patch")

df = pd.DataFrame(dados_torres)

# Estilização para destacar o valor que deve ser digitado no processador
st.dataframe(
    df.style.format("{:.2f}", subset=["VALOR DSP (ms)", "Dist. Virtual (m)"])
    .highlight_max(axis=0, subset=['VALOR DSP (ms)'], color='#1e3d3d'),
    use_container_width=True
)

# --- BOTÃO DE DOWNLOAD (Útil para documentação do show) ---
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="📥 Baixar Mapa de Delay (CSV)",
    data=csv,
    file_name='mapa_delay_show.csv',
    mime='text/csv',
)

st.markdown("---")
st.caption("Engenharia de Sistemas de Áudio - Cálculo baseado na norma ISO 9613-1.")
