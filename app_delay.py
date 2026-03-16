import streamlit as st
import pandas as pd

# Configuração da Página
st.set_page_config(page_title="AudioAlign Multi-Tower Pro", page_icon="🔊", layout="wide")

def calcular_v_som(t):
    return 331.3 + (0.606 * t)

st.title("🔊 AudioAlign Multi-Tower Pro")
st.markdown("### Gestão de Alinhamento para Múltiplas Torres de Delay")

# --- BARRA LATERAL: PARÂMETROS GLOBAIS ---
st.sidebar.header("🌡️ Parâmetros Ambientais")
temp = st.sidebar.slider("Temperatura Local (°C)", -10.0, 50.0, 25.0, 0.5)
v_som = calcular_v_som(temp)

st.sidebar.markdown("---")
st.sidebar.header("🛠️ Ajustes Globais")
haas_global = st.sidebar.slider("Haas Offset Padrão (ms)", 0.0, 20.0, 7.0)
latencia_dsp = st.sidebar.number_input("Latência do Processador (ms)", 0.0, 5.0, 0.0, 0.1)

# --- CONFIGURAÇÃO DAS TORRES ---
st.markdown("---")
num_torres = st.number_input("Quantidade de Torres de Delay", min_value=1, max_value=20, value=2)

st.markdown("#### Insira a distância de cada torre em relação ao Main PA (Palco)")

# Criar uma lista para armazenar os dados das torres
dados_torres = []

# Layout de colunas dinâmicas para entrada de dados
for i in range(int(num_torres)):
    with st.expander(f"📍 Configuração da Torre {i+1}", expanded=True):
        col1, col2, col3 = st.columns([2, 2, 1])
        
        with col1:
            nome = st.text_input(f"Identificação da Torre", value=f"Torre {i+1}", key=f"nome_{i}")
        with col2:
            distancia = st.number_input(f"Distância do Palco (Metros)", min_value=0.0, value=20.0 + (i*15), step=0.1, key=f"dist_{i}")
        with col3:
            haas_individual = st.number_input(f"Haas Extra (ms)", value=haas_global, key=f"haas_{i}")

        # Cálculos para esta torre específica
        tempo_propagacao = (distancia / v_som) * 1000
        delay_total = tempo_propagacao + haas_individual - latencia_dsp
        distancia_virtual = (delay_total / 1000) * v_som
        
        dados_torres.append({
            "Torre": nome,
            "Distância Real (m)": distancia,
            "Tempo de Percurso (ms)": round(tempo_propagacao, 2),
            "Haas (ms)": haas_individual,
            "DELAY NO PROCESSADOR (ms)": round(delay_total, 2),
            "Distância Virtual (m)": round(distancia_virtual, 2)
        })

# --- TABELA DE RESUMO PARA O ENGENHEIRO ---
st.markdown("---")
st.subheader("📋 Mapa de Configuração (Patch de Delay)")

df = pd.DataFrame(dados_torres)

# Destacar a coluna principal
st.dataframe(df.style.highlight_max(axis=0, subset=['DELAY NO PROCESSADOR (ms)'], color='#2e3333'), use_container_width=True)

# --- VISUALIZAÇÃO GRÁFICA ---
st.markdown("### 📊 Comparativo de Profundidade Acústica")
st.bar_chart(df.set_index("Torre")[["Distância Real (m)", "Distância Virtual (m)"]])

# --- RODAPÉ TÉCNICO ---
st.info(f"💡 Velocidade do Som hoje: {v_som:.2f} m/s. Lembre-se de conferir a fase com Ruído Rosa em cada ponto de transição entre torres.")
