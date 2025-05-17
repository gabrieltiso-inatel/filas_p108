import os
import platform

from queues.mmsn.input import get_queue_data
from queues.mmsn.queue import MM1NQueue

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def display_menu():
    print("\nMenu de Opções:")
    print("1. Probabilidade de zero clientes no sistema (P0)")
    print("2. Probabilidade de n clientes no sistema (Pn)")
    print("3. Número médio de clientes na fila (Lq)")
    print("4. Tempo médio de espera na fila (Wq)")
    print("5. Número médio de clientes no sistema (L)")
    print("6. Tempo médio gasto no sistema (W))")
    print("7. Sair")


def handle_mm1n_queue(queue: MM1NQueue):
    while True:
        display_menu()
        choice = int(input("Escolha uma opção: "))
        clear_screen()

        if choice == 1:
            result = queue.prob_zero_clients_in_system()
            print(f"Probabilidade de 0 clientes no sistema (P0): {result:.2f}")
        elif choice == 2:
            n = int(input("Digite o valor de n: "))
            result = queue.prob_n_clients_in_system(n)
            print(f"Probabilidade de {n} clientes no sistema (Pn): {result:.2f}")
            break
        elif choice == 3:
            result = queue.avg_number_clients_in_queue()
            print(f"Número médio de clientes na fila (Lq): {result:.2f}")
        elif choice == 4:
            result = queue.avg_waiting_time_in_queue()
            print(f"Tempo médio de espera na fila (Wq): {result:.2f}")
        elif choice == 5:
            result = queue.avg_number_clients_in_system()
            print(f"Número médio de clientes no sistema (L): {result:.2f}")
        elif choice == 6:
            result = queue.avg_time_in_system()
            print(f"Tempo médio gasto no sistema (W): {result:.2f}")
        elif choice == 7:
            print("Saindo do simulador...")
            break
        else:
            print("Opção inválida. Tente novamente.")

        input("Pressione Enter para continuar...")
        clear_screen()


def run():
    print("Bem-vindo ao simulador de filas M/M/s/N!")
    params = get_queue_data()

    print(f"\nParâmetros da fila:\n {params}")

    if params.s == 1:
        queue = MM1NQueue(params)
        handle_mm1n_queue(queue)
    else:
        queue = MMsNQueue(params)
        handle_mmsn_queue(queue)