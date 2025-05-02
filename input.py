import os
from queue_input_data import QueueInputData

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

class InputCollector:
    def collect(self) -> QueueInputData:
        clear_terminal()
        print("Bem-vindo ao Simulador de Filas\n")

        A = input("Distribuição de Chegada (M, D, Ek, G): ").strip().upper()
        B = input("Distribuição de Serviço (M, D, Ek, G): ").strip().upper()
        m = int(input("Número de Servidores (m): "))
        C = input("Disciplina da Fila (FCFS, LCFS, SIRO) [padrão=FCFS]: ").strip().upper() or "FCFS"

        K_input = input("Capacidade Máxima (K) [Enter = ∞]: ")
        K = int(K_input) if K_input else None

        N_input = input("Tamanho da População (N) [Enter = ∞]: ")
        N = int(N_input) if N_input else None

        lambda_param = float(input("Taxa de Chegada (λ): "))
        mi_param = float(input("Taxa de Serviço (μ): "))

        return QueueInputData(
            A=A,
            B=B,
            m=m,
            C=C,
            K=K,
            N=N,
            lambda_param=lambda_param,
            mi_param=mi_param
        )
