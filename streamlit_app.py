import streamlit as st
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from interfaces.mg1_interface import mg1_interface
from interfaces.mms_interface import mms_interface
from interfaces.mmsn_interface import mmsn_interface
from interfaces.mmsk_interface import mmsk_interface
from interfaces.priority_single_interface import priority_single_server_interface
from interfaces.priority_multiple_interface import priority_multiple_servers_interface

st.set_page_config(
    page_title="Calculadora de Teoria de Filas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("🔢 Calculadora de Teoria de Filas")
st.markdown("Calcule métricas para vários modelos de filas com precisão de 8 casas decimais")
st.info("💡 **Dica**: Todos os campos de entrada suportam valores com até 8 casas decimais para máxima precisão.")

st.sidebar.title("Modelos de Filas")
st.sidebar.markdown("Selecione o tipo de fila que deseja analisar:")

model_type = st.sidebar.selectbox(
    "Modelo de Fila",
    [
        "Fila M/G/1",
        "Fila M/M/s", 
        "Fila M/M/s/n",
        "Fila M/M/s/K",
        "Fila de Prioridade (Servidor Único)",
        "Fila de Prioridade (Múltiplos Servidores)"
    ]
)

# Add model descriptions in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Descrições dos Modelos:")

model_descriptions = {
    "Fila M/G/1": "Chegadas Poisson, distribuição geral de serviço, 1 servidor",
    "Fila M/M/s": "Chegadas Poisson, serviço exponencial, s servidores",
    "Fila M/M/s/n": "M/M/s com capacidade limitada do sistema",
    "Fila M/M/s/K": "M/M/s com capacidade limitada e perda de clientes",
    "Fila de Prioridade (Servidor Único)": "Fila com prioridades preemptivas, 1 servidor",
    "Fila de Prioridade (Múltiplos Servidores)": "Fila com prioridades preemptivas, múltiplos servidores"
}

st.sidebar.info(model_descriptions[model_type])

# Additional information in sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### Notação:")
st.sidebar.markdown("""
- **λ**: Taxa de chegada
- **μ**: Taxa de serviço  
- **s**: Número de servidores
- **ρ**: Utilização do sistema
- **L**: Número médio de clientes no sistema
- **Lq**: Número médio de clientes na fila
- **W**: Tempo médio no sistema
- **Wq**: Tempo médio na fila
- **P₀**: Probabilidade do sistema vazio
""")

st.markdown("---")

if model_type == "Fila M/G/1":
    mg1_interface()
elif model_type == "Fila M/M/s":
    mms_interface()
elif model_type == "Fila M/M/s/n":
    mmsn_interface()
elif model_type == "Fila M/M/s/K":
    mmsk_interface()
elif model_type == "Fila de Prioridade (Servidor Único)":
    priority_single_server_interface()
elif model_type == "Fila de Prioridade (Múltiplos Servidores)":
    priority_multiple_servers_interface()

st.markdown("---")
st.markdown("""
<div style='text-align: center'>
    <p>📚 <strong>Calculadora de Teoria de Filas</strong></p>
</div>
""", unsafe_allow_html=True)
