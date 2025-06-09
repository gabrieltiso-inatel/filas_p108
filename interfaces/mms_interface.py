import streamlit as st
import pandas as pd
import plotly.express as px
from typing import Dict, Any
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.service import StreamlitQueueService

def display_results(results: Dict[str, Any], title: str):
    """Display M/M/s queue calculation results"""
    st.subheader(f"📈 {title}")
    
    metric_translations = {
        'prob_zero_clients': 'Probabilidade Zero Clientes (P₀)',
        'avg_clients_in_queue': 'Clientes Médios na Fila (Lq)',
        'avg_wait_time_in_queue': 'Tempo Médio na Fila (Wq)',
        'avg_clients_in_system': 'Clientes Médios no Sistema (L)',
        'avg_wait_time_in_system': 'Tempo Médio no Sistema (W)',
        'prob_system_busy': 'Probabilidade Sistema Ocupado (ρ)'
    }
    
    cols = st.columns(3)
    for i, (key, value) in enumerate(results.items()):
        with cols[i % 3]:
            formatted_key = metric_translations.get(key, key.replace('_', ' ').title())
            if isinstance(value, float):
                st.metric(formatted_key, f"{value:.8f}")
            else:
                st.metric(formatted_key, str(value))

def mms_interface():
    st.header("Calculadora de Fila M/M/s")
    st.markdown("Fila multi-servidor com chegadas Poisson e tempos de serviço exponenciais")
    
    # Service initialization
    service = StreamlitQueueService()
    
    # Input parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.00000001, value=3.0, step=0.00000001, format="%.8f", key="mms_lambda")
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.00000001, value=2.0, step=0.00000001, format="%.8f", key="mms_mu")
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=1, value=2, step=1, key="mms_servers")
    
    # System utilization info
    rho = lmbd / (s * mu)
    st.info(f"Utilização do sistema (ρ): {rho:.8f}")
    
    if rho >= 1:
        st.error("⚠️ Sistema instável! A utilização (ρ) deve ser menor que 1 para o sistema ser estável.")
    
    # Additional calculations
    st.subheader("Cálculos Adicionais")
    calc_prob_n = st.checkbox("Calcular P(n clientes no sistema)", key="mms_calc_prob_n")
    calc_prob_wait = st.checkbox("Calcular P(tempo de espera > t)", key="mms_calc_prob_wait")
    
    n_clients = 0
    wait_time = 0.0
    wait_type = "sistema"
    
    if calc_prob_n:
        n_clients = st.number_input("Número de clientes (n)", min_value=0, value=5, step=1, key="mms_n_clients")
    
    if calc_prob_wait:
        col1, col2 = st.columns(2)
        with col1:
            wait_time = st.number_input("Limiar de tempo (t)", min_value=0.0, value=1.0, step=0.00000001, format="%.8f", key="mms_wait_time")
        with col2:
            wait_type = st.selectbox("Tipo de tempo de espera", ["sistema", "fila"], key="mms_wait_type")
    
    if st.button("Calcular M/M/s", key="mms_calculate"):
        try:
            if rho >= 1:
                st.error("Não é possível calcular métricas para sistema instável.")
            else:
                results = service.calculate_mms(lmbd, mu, s)
                display_results(results, "Resultados M/M/s")
                
                # Additional calculations results
                if calc_prob_n:
                    prob_n = service.calculate_mms_prob_n(lmbd, mu, s, n_clients)
                    st.metric(f"P({n_clients} clientes no sistema)", f"{prob_n:.8f}")
                
                if calc_prob_wait:
                    wait_type_eng = "system" if wait_type == "sistema" else "queue"
                    prob_wait = service.calculate_mms_prob_wait(lmbd, mu, s, wait_time, wait_type_eng)
                    st.metric(f"P(espera no {wait_type} > {wait_time})", f"{prob_wait:.8f}")
                
                # Additional visualization
                st.subheader("📊 Visualização das Métricas")
                
                # Create a comparison chart
                metrics_df = pd.DataFrame({
                    'Métrica': ['Clientes na Fila (Lq)', 'Clientes no Sistema (L)', 'Tempo na Fila (Wq)', 'Tempo no Sistema (W)'],
                    'Valor': [
                        results['avg_clients_in_queue'],
                        results['avg_clients_in_system'],
                        results['avg_wait_time_in_queue'],
                        results['avg_wait_time_in_system']
                    ],
                    'Tipo': ['Número de Clientes', 'Número de Clientes', 'Tempo', 'Tempo']
                })
                
                fig = px.bar(
                    metrics_df, 
                    x='Métrica', 
                    y='Valor', 
                    color='Tipo',
                    title=f"Métricas da Fila M/M/{s}"
                )
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

if __name__ == "__main__":
    mms_interface()
