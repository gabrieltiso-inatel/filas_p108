import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, Any
import sys
import os

# Add the current directory to the path to find the app module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.service import StreamlitQueueService

# Configure the page
st.set_page_config(
    page_title="Calculadora de Teoria de Filas",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize service
@st.cache_resource
def get_service():
    return StreamlitQueueService()

service = get_service()

# Main title
st.title("🔢 Calculadora de Teoria de Filas")
st.markdown("Calcule métricas para vários modelos de filas")

# Sidebar for model selection
st.sidebar.title("Modelos de Filas")
model_type = st.sidebar.selectbox(
    "Selecione o Modelo de Fila",
    [
        "Fila M/G/1",
        "Fila M/M/s", 
        "Fila M/M/s/n",
        "Fila M/M/s/K",
        "Fila de Prioridade (Servidor Único)",
        "Fila de Prioridade (Múltiplos Servidores)"
    ]
)

# Helper function to display results
def display_results(results: Dict[str, Any], title: str):
    st.subheader(f"📈 {title}")
    
    # Create columns for metrics
    if isinstance(list(results.values())[0], list):
        # Priority queue results (arrays) - Show all classes in table
        n_classes = len(list(results.values())[0])
        
        # Create DataFrame for all priority classes
        df_results = pd.DataFrame({
            'Classe de Prioridade': [f"Prioridade {i+1}" for i in range(n_classes)],
            'Tempo Médio no Sistema (W)': [f"{val:.5f}" for val in results['avg_waiting_time_in_system']],
            'Tempo Médio na Fila (Wq)': [f"{val:.5f}" for val in results['avg_waiting_time_in_queue']],
            'Clientes Médios no Sistema (L)': [f"{val:.5f}" for val in results['avg_clients_in_system']],
            'Clientes Médios na Fila (Lq)': [f"{val:.5f}" for val in results['avg_clients_in_queue']]
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
        
    else:
        # Regular queue results (single values)
        metric_translations = {
            'prob_zero_clients': 'Probabilidade Zero Clientes (P₀)',
            'avg_clients_in_queue': 'Clientes Médios na Fila (Lq)',
            'avg_wait_time_in_queue': 'Tempo Médio na Fila (Wq)',
            'avg_clients_in_system': 'Clientes Médios no Sistema (L)',
            'avg_wait_time_in_system': 'Tempo Médio no Sistema (W)',
            'prob_system_busy': 'Probabilidade Sistema Ocupado (ρ)',
            'avg_effective_arrival_rate': 'Taxa de Chegada Efetiva (λₑ)'
        }
        
        cols = st.columns(min(4, len(results)))
        for i, (key, value) in enumerate(results.items()):
            with cols[i % 4]:
                formatted_key = metric_translations.get(key, key.replace('_', ' ').title())
                if isinstance(value, float):
                    st.metric(formatted_key, f"{value:.5f}")
                else:
                    st.metric(formatted_key, str(value))

# M/G/1 Queue
if model_type == "Fila M/G/1":
    st.header("Calculadora de Fila M/G/1")
    st.markdown("Fila de servidor único com chegadas Poisson e distribuição geral de tempo de serviço")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.01, value=2.0, step=0.1)
    with col2:
        avg_service_time = st.number_input("Tempo Médio de Serviço", min_value=0.01, value=0.4, step=0.1)
    with col3:
        service_time_variance = st.number_input("Variância do Tempo de Serviço (σ²)", min_value=0.01, value=0.1, step=0.01)
    
    if st.button("Calcular M/G/1"):
        try:
            results = service.calculate_mg1(lmbd, avg_service_time, service_time_variance)
            display_results(results, "Resultados M/G/1")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# M/M/s Queue
elif model_type == "Fila M/M/s":
    st.header("Calculadora de Fila M/M/s")
    st.markdown("Fila multi-servidor com chegadas Poisson e tempos de serviço exponenciais")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.01, value=3.0, step=0.1)
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.01, value=2.0, step=0.1)
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=1, value=2, step=1)
    
    # Additional calculations
    st.subheader("Cálculos Adicionais")
    calc_prob_n = st.checkbox("Calcular P(n clientes no sistema)")
    calc_prob_wait = st.checkbox("Calcular P(tempo de espera > t)")
    
    n_clients = 0
    wait_time = 0.0
    wait_type = "sistema"
    
    if calc_prob_n:
        n_clients = st.number_input("Número de clientes (n)", min_value=0, value=5, step=1)
    
    if calc_prob_wait:
        col1, col2 = st.columns(2)
        with col1:
            wait_time = st.number_input("Limiar de tempo (t)", min_value=0.0, value=1.0, step=0.1)
        with col2:
            wait_type = st.selectbox("Tipo de tempo de espera", ["sistema", "fila"])
    
    if st.button("Calcular M/M/s"):
        try:
            results = service.calculate_mms(lmbd, mu, s)
            display_results(results, "Resultados M/M/s")
            
            if calc_prob_n:
                prob_n = service.calculate_mms_prob_n(lmbd, mu, s, n_clients)
                st.metric(f"P({n_clients} clientes no sistema)", f"{prob_n:.5f}")
            
            if calc_prob_wait:
                wait_type_eng = "system" if wait_type == "sistema" else "queue"
                prob_wait = service.calculate_mms_prob_wait(lmbd, mu, s, wait_time, wait_type_eng)
                st.metric(f"P(espera no {wait_type} > {wait_time})", f"{prob_wait:.5f}")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# M/M/s/n Queue
elif model_type == "Fila M/M/s/n":
    st.header("Calculadora de Fila M/M/s/n")
    st.markdown("Fila multi-servidor com capacidade limitada do sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.01, value=3.0, step=0.1)
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.01, value=2.0, step=0.1)
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=1, value=2, step=1)
    with col4:
        n = st.number_input("Capacidade do Sistema (n)", min_value=1, value=10, step=1)
    
    calc_prob_n = st.checkbox("Calcular P(n clientes no sistema)")
    if calc_prob_n:
        target_n = st.number_input("Número alvo de clientes", min_value=0, value=5, step=1)
    
    if st.button("Calcular M/M/s/n"):
        try:
            results = service.calculate_mmsn(lmbd, mu, s, n)
            display_results(results, "Resultados M/M/s/n")
            
            if calc_prob_n:
                prob_n = service.calculate_mmsn_prob_n(lmbd, mu, s, n, target_n)
                st.metric(f"P({target_n} clientes no sistema)", f"{prob_n:.5f}")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# M/M/s/K Queue
elif model_type == "Fila M/M/s/K":
    st.header("Calculadora de Fila M/M/s/K")
    st.markdown("Fila multi-servidor com capacidade limitada e perda de clientes")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        lmbd = st.number_input("Taxa de Chegada (λ)", min_value=0.01, value=3.0, step=0.1)
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.01, value=2.0, step=0.1)
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=1, value=2, step=1)
    with col4:
        K = st.number_input("Capacidade do Sistema (K)", min_value=1, value=8, step=1)
    
    calc_prob_n = st.checkbox("Calcular P(n clientes no sistema)")
    if calc_prob_n:
        target_n = st.number_input("Número alvo de clientes", min_value=0, value=5, step=1)
    
    if st.button("Calcular M/M/s/K"):
        try:
            results = service.calculate_mmsk(lmbd, mu, s, K)
            display_results(results, "Resultados M/M/s/K")
            
            if calc_prob_n:
                prob_n = service.calculate_mmsk_prob_n(lmbd, mu, s, K, target_n)
                st.metric(f"P({target_n} clientes no sistema)", f"{prob_n:.5f}")
                
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# Priority Queue (Single Server)
elif model_type == "Fila de Prioridade (Servidor Único)":
    st.header("Calculadora de Fila de Prioridade - Servidor Único")
    st.markdown("Fila de prioridade preemptiva com interrupção")
    
    col1, col2 = st.columns(2)
    with col1:
        n = st.number_input("Número de Classes de Prioridade", min_value=1, value=3, step=1)
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.01, value=2.0, step=0.1)
    with col2:
        s = 1  # Single server
        st.write(f"Número de Servidores: {s}")
    
    st.subheader("Taxas de Chegada por Classe de Prioridade")
    st.markdown("*Classes com menor número têm maior prioridade*")
    
    lmbds = []
    cols = st.columns(min(n, 4))
    for i in range(n):
        with cols[i % 4]:
            lmbd_i = st.number_input(f"λ{i+1} (Prioridade {i+1})", min_value=0.01, value=0.5 + i*0.3, step=0.1, key=f"lmbd_{i}")
            lmbds.append(lmbd_i)
    
    total_lambda = sum(lmbds)
    rho = total_lambda / (s * mu)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Taxa de chegada total (λ): {total_lambda:.3f}")
    with col2:
        st.info(f"Utilização do sistema (ρ): {rho:.3f}")
    
    if rho >= 1:
        st.error("⚠️ Sistema instável! A utilização (ρ) deve ser menor que 1 para o sistema ser estável.")
    
    if st.button("Calcular Fila de Prioridade (Servidor Único)"):
        try:
            if rho >= 1:
                st.error("Não é possível calcular métricas para sistema instável.")
            else:
                results = service.calculate_priority_single_server(n, lmbds, mu, s, total_lambda)
                display_results(results, "Resultados da Fila de Prioridade (Servidor Único)")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# Priority Queue (Multiple Servers)
elif model_type == "Fila de Prioridade (Múltiplos Servidores)":
    st.header("Calculadora de Fila de Prioridade - Múltiplos Servidores")
    st.markdown("Fila de prioridade preemptiva com interrupção e múltiplos servidores")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        n = st.number_input("Número de Classes de Prioridade", min_value=1, value=3, step=1)
    with col2:
        mu = st.number_input("Taxa de Serviço (μ)", min_value=0.01, value=2.0, step=0.1)
    with col3:
        s = st.number_input("Número de Servidores (s)", min_value=2, value=3, step=1)
    
    st.subheader("Taxas de Chegada por Classe de Prioridade")
    st.markdown("*Classes com menor número têm maior prioridade*")
    
    lmbds = []
    cols = st.columns(min(n, 4))
    for i in range(n):
        with cols[i % 4]:
            lmbd_i = st.number_input(f"λ{i+1} (Prioridade {i+1})", min_value=0.01, value=0.5 + i*0.3, step=0.1, key=f"lmbd_multi_{i}")
            lmbds.append(lmbd_i)
    
    total_lambda = sum(lmbds)
    rho = total_lambda / (s * mu)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"Taxa de chegada total (λ): {total_lambda:.3f}")
    with col2:
        st.info(f"Utilização do sistema (ρ): {rho:.3f}")
    
    if rho >= 1:
        st.error("⚠️ Sistema instável! A utilização (ρ) deve ser menor que 1 para o sistema ser estável.")
    
    if st.button("Calcular Fila de Prioridade (Múltiplos Servidores)"):
        try:
            if rho >= 1:
                st.error("Não é possível calcular métricas para sistema instável.")
            else:
                results = service.calculate_priority_multiple_servers(n, lmbds, mu, s, total_lambda)
                display_results(results, "Resultados da Fila de Prioridade (Múltiplos Servidores)")
        except Exception as e:
            st.error(f"Erro: {str(e)}")

# Footer
st.markdown("---")
st.markdown("📚 Calculadora de Teoria de Filas")