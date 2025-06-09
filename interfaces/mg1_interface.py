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
    """Display M/G/1 queue calculation results"""
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

def mg1_interface():
    st.header("Calculadora de Fila M/G/1")
    st.markdown("Fila de servidor único com chegadas Poisson e distribuição geral de tempo de serviço")
    
    # Service initialization
    service = StreamlitQueueService()
    
    # Input parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.00000001, value=2.0, step=0.00000001, format="%.8f", key="mg1_lambda")
    with col2:
        avg_service_time = st.number_input("Tempo Médio de Serviço", min_value=0.00000001, value=0.4, step=0.00000001, format="%.8f", key="mg1_service_time")
    with col3:
        service_time_variance = st.number_input("Variância do Tempo de Serviço (σ²)", min_value=0.00000001, value=0.1, step=0.00000001, format="%.8f", key="mg1_variance")
    
    # System utilization info
    rho = lmbd * avg_service_time
    st.info(f"Utilização do sistema (ρ): {rho:.8f}")
    
    if rho >= 1:
        st.error("⚠️ Sistema instável! A utilização (ρ) deve ser menor que 1 para o sistema ser estável.")
    
    if st.button("Calcular M/G/1", key="mg1_calculate"):
        try:
            if rho >= 1:
                st.error("Não é possível calcular métricas para sistema instável.")
            else:
                results = service.calculate_mg1(lmbd, avg_service_time, service_time_variance)
                display_results(results, "Resultados M/G/1")
                
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
                    title="Métricas da Fila M/G/1"
                )
                st.plotly_chart(fig, use_container_width=True)
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

if __name__ == "__main__":
    mg1_interface()
