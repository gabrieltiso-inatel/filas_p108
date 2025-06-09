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
    """Display M/M/s/n queue calculation results"""
    st.subheader(f"📈 {title}")
    
    metric_translations = {
        'prob_zero_clients': 'Probabilidade Zero Clientes (P₀)',
        'avg_clients_in_queue': 'Clientes Médios na Fila (Lq)',
        'avg_wait_time_in_queue': 'Tempo Médio na Fila (Wq)',
        'avg_clients_in_system': 'Clientes Médios no Sistema (L)',
        'avg_wait_time_in_system': 'Tempo Médio no Sistema (W)'
    }
    
    cols = st.columns(3)
    for i, (key, value) in enumerate(results.items()):
        with cols[i % 3]:
            formatted_key = metric_translations.get(key, key.replace('_', ' ').title())
            if isinstance(value, float):
                st.metric(formatted_key, f"{value:.8f}")
            else:
                st.metric(formatted_key, str(value))

def mmsn_interface():
    st.header("Calculadora de Fila M/M/s/n")
    st.markdown("Fila multi-servidor com capacidade limitada do sistema")
    
    # Service initialization
    service = StreamlitQueueService()
    
    # Input parameters
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.00000001, value=3.0, step=0.00000001, format="%.8f", key="mmsn_lambda")
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.00000001, value=2.0, step=0.00000001, format="%.8f", key="mmsn_mu")
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=1, value=2, step=1, key="mmsn_servers")
    with col4:
        n = st.number_input("Capacidade do Sistema (n)", min_value=1, value=10, step=1, key="mmsn_capacity")
    
    # System info
    traffic_intensity = lmbd / mu
    st.info(f"Intensidade de tráfico (λ/μ): {traffic_intensity:.8f}")
    
    if n < s:
        st.error("⚠️ A capacidade do sistema (n) deve ser maior ou igual ao número de servidores (s)!")
    
    # Additional calculations
    st.subheader("Cálculos Adicionais")
    calc_prob_n = st.checkbox("Calcular P(n clientes no sistema)", key="mmsn_calc_prob_n")
    
    if calc_prob_n:
        target_n = st.number_input("Número alvo de clientes", min_value=0, max_value=n, value=min(5, n), step=1, key="mmsn_target_n")
    
    if st.button("Calcular M/M/s/n", key="mmsn_calculate"):
        try:
            if n < s:
                st.error("Não é possível calcular métricas: capacidade deve ser ≥ número de servidores.")
            else:
                results = service.calculate_mmsn(lmbd, mu, s, n)
                display_results(results, f"Resultados M/M/{s}/{n}")
                
                # Additional calculations results
                if calc_prob_n:
                    prob_n = service.calculate_mmsn_prob_n(lmbd, mu, s, n, target_n)
                    st.metric(f"P({target_n} clientes no sistema)", f"{prob_n:.8f}")
                
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
                    title=f"Métricas da Fila M/M/{s}/{n}"
                )
                st.plotly_chart(fig, use_container_width=True)
                
                # System state probabilities chart
                if calc_prob_n:
                    st.subheader("📉 Distribuição de Probabilidades")
                    prob_data = []
                    for i in range(n + 1):
                        prob_i = service.calculate_mmsn_prob_n(lmbd, mu, s, n, i)
                        prob_data.append({'Número de Clientes': i, 'Probabilidade': prob_i})
                    
                    prob_df = pd.DataFrame(prob_data)
                    fig_prob = px.bar(
                        prob_df,
                        x='Número de Clientes',
                        y='Probabilidade',
                        title=f"Distribuição de Probabilidades - M/M/{s}/{n}"
                    )
                    st.plotly_chart(fig_prob, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

if __name__ == "__main__":
    mmsn_interface()
