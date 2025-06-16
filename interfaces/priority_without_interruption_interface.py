import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any, List
import sys
import os

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.service import StreamlitQueueService

def display_priority_results(results: Dict[str, Any], title: str, n_classes: int):
    """Display priority queue calculation results"""
    st.subheader(f"📈 {title}")
    
    # Create DataFrame for all priority classes
    df_results = pd.DataFrame({
        'Classe de Prioridade': [f"Prioridade {i+1}" for i in range(n_classes)],
        'Tempo Médio no Sistema (W)': [f"{val:.8f}" for val in results['avg_waiting_time_in_system']],
        'Tempo Médio na Fila (Wq)': [f"{val:.8f}" for val in results['avg_waiting_time_in_queue']],
        'Clientes Médios no Sistema (L)': [f"{val:.8f}" for val in results['avg_clients_in_system']],
        'Clientes Médios na Fila (Lq)': [f"{val:.8f}" for val in results['avg_clients_in_queue']]
    })
    
    # Display the table
    st.subheader("📊 Resultados por Classe de Prioridade")
    st.dataframe(df_results, use_container_width=True)
    
    # Create comprehensive comparison charts
    st.subheader("📈 Comparação Visual das Métricas")
    
    # Prepare data for plotting
    plot_df = pd.DataFrame({
        'Classe de Prioridade': range(1, n_classes + 1),
        'Tempo no Sistema (W)': results['avg_waiting_time_in_system'],
        'Tempo na Fila (Wq)': results['avg_waiting_time_in_queue'],
        'Clientes no Sistema (L)': results['avg_clients_in_system'],
        'Clientes na Fila (Lq)': results['avg_clients_in_queue']
    })
    
    # Create two columns for charts
    col1, col2 = st.columns(2)
    
    with col1:
        # Waiting times comparison
        fig_times = px.bar(
            plot_df, 
            x='Classe de Prioridade', 
            y=['Tempo no Sistema (W)', 'Tempo na Fila (Wq)'], 
            title="Tempos de Espera por Classe de Prioridade",
            barmode='group',
            labels={'value': 'Tempo', 'variable': 'Métrica'}
        )
        fig_times.update_layout(xaxis_title="Classe de Prioridade", yaxis_title="Tempo")
        st.plotly_chart(fig_times, use_container_width=True)
    
    with col2:
        # Number of clients comparison
        fig_clients = px.bar(
            plot_df, 
            x='Classe de Prioridade', 
            y=['Clientes no Sistema (L)', 'Clientes na Fila (Lq)'], 
            title="Número de Clientes por Classe de Prioridade",
            barmode='group',
            labels={'value': 'Número de Clientes', 'variable': 'Métrica'}
        )
        fig_clients.update_layout(xaxis_title="Classe de Prioridade", yaxis_title="Número de Clientes")
        st.plotly_chart(fig_clients, use_container_width=True)
    
    # Additional line chart for trends
    st.subheader("📉 Tendências das Métricas")
    fig_lines = go.Figure()
    
    fig_lines.add_trace(go.Scatter(
        x=plot_df['Classe de Prioridade'], 
        y=plot_df['Tempo no Sistema (W)'],
        mode='lines+markers',
        name='Tempo no Sistema (W)',
        line=dict(color='blue')
    ))
    
    fig_lines.add_trace(go.Scatter(
        x=plot_df['Classe de Prioridade'], 
        y=plot_df['Tempo na Fila (Wq)'],
        mode='lines+markers',
        name='Tempo na Fila (Wq)',
        line=dict(color='red')
    ))
    
    fig_lines.add_trace(go.Scatter(
        x=plot_df['Classe de Prioridade'], 
        y=plot_df['Clientes no Sistema (L)'],
        mode='lines+markers',
        name='Clientes no Sistema (L)',
        line=dict(color='green'),
        yaxis='y2'
    ))
    
    fig_lines.add_trace(go.Scatter(
        x=plot_df['Classe de Prioridade'], 
        y=plot_df['Clientes na Fila (Lq)'],
        mode='lines+markers',
        name='Clientes na Fila (Lq)',
        line=dict(color='orange'),
        yaxis='y2'
    ))
    
    # Update layout for dual y-axis
    fig_lines.update_layout(
        title="Evolução das Métricas por Classe de Prioridade",
        xaxis_title="Classe de Prioridade",
        yaxis=dict(title="Tempo", side="left"),
        yaxis2=dict(title="Número de Clientes", side="right", overlaying="y"),
        legend=dict(x=0.02, y=0.98)
    )
    
    st.plotly_chart(fig_lines, use_container_width=True)

def priority_without_interruption_interface():
    st.header("Calculadora de Fila de Prioridade - Sem Interrupção")
    st.markdown("Fila de prioridade não-preemptiva (sem interrupção)")
    
    # Service initialization
    service = StreamlitQueueService()
    
    # Input parameters
    col1, col2, col3 = st.columns(3)
    with col1:
        n = st.number_input("Número de Classes de Prioridade", min_value=1, max_value=10, value=3, step=1, key="priority_no_interrupt_n")
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.00000001, value=3.0, step=0.00000001, format="%.8f", key="priority_no_interrupt_mu")
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=1, max_value=10, value=1, step=1, key="priority_no_interrupt_servers")
    
    st.markdown("*Classes com menor número têm maior prioridade (disciplina não-preemptiva)*")
    
    st.subheader("Taxas de Chegada por Classe de Prioridade")
    
    # Dynamic input for lambda values
    lmbds = []
    cols = st.columns(min(n, 4))
    for i in range(n):
        with cols[i % 4]:
            lmbd_i = st.number_input(
                f"λ{i+1} (Prioridade {i+1})", 
                min_value=0.00000001, 
                value=0.2 + i*0.5, 
                step=0.00000001, 
                format="%.8f",
                key=f"priority_no_interrupt_lmbd_{i}"
            )
            lmbds.append(lmbd_i)
    
    total_lambda = sum(lmbds)
    rho = total_lambda / (s * mu)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Taxa de chegada total (λ): {total_lambda:.8f}")
    with col2:
        st.info(f"Utilização do sistema (ρ): {rho:.8f}")
    
    # Stability check for without interruption
    if total_lambda >= s * mu:
        st.error("⚠️ Sistema instável! Para filas sem interrupção: ∑λᵢ < s×μ")
    elif rho >= 1:
        st.warning("⚠️ Sistema próximo da instabilidade!")
    
    # Summary table of arrivals per priority
    st.subheader("📋 Resumo das Classes de Prioridade")
    arrivals_df = pd.DataFrame({
        'Classe': [f"Prioridade {i+1}" for i in range(n)],
        'Taxa de Chegada (λ)': [f"{lmbd:.8f}" for lmbd in lmbds],
        'Percentual do Total': [f"{(lmbd/total_lambda)*100:.2f}%" for lmbd in lmbds]
    })
    st.dataframe(arrivals_df, use_container_width=True)
    
    # System capacity analysis
    st.subheader("📊 Análise de Capacidade")
    total_capacity = s * mu
    utilization_percentage = (total_lambda / total_capacity) * 100
    
    capacity_df = pd.DataFrame({
        'Métrica': ['Capacidade Total do Sistema', 'Demanda Total', 'Utilização'],
        'Valor': [f"{total_capacity:.8f}", f"{total_lambda:.8f}", f"{utilization_percentage:.2f}%"]
    })
    st.dataframe(capacity_df, use_container_width=True)
    
    # Important note about the difference
    st.info("""
    📝 **Diferença entre Modelos de Prioridade:**
    - **Com Interrupção (Preemptivo)**: Clientes de alta prioridade podem interromper o atendimento de clientes de baixa prioridade
    - **Sem Interrupção (Não-Preemptivo)**: Clientes de alta prioridade aguardam o término do atendimento atual antes de serem servidos
    """)
    
    if st.button("Calcular Fila de Prioridade (Sem Interrupção)", key="priority_no_interrupt_calculate"):
        try:
            if total_lambda >= s * mu:
                st.error("Não é possível calcular métricas para sistema instável.")
            else:
                results = service.calculate_priority_without_interruption(n, lmbds, mu, s, total_lambda)
                display_priority_results(results, f"Resultados da Fila de Prioridade Sem Interrupção ({s} Servidor{'es' if s > 1 else ''})", n)
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

if __name__ == "__main__":
    priority_without_interruption_interface()
