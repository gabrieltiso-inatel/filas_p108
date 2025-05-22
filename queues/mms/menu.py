import os
import platform

from queues.mms.input import get_queue_data
from queues.mms.queue import MM1Queue, MMsQueue

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def display_menu():
    print("\nMenu de Opções:")
    print("1. Probabilidade de n clientes no sistema (Pn)")
    print("2. Probabilidade de o sistema estar vazio (P0)")
    print("3. Probabilidade de o sistema estar ocupado (1 - P0)")
    print("4. Número médio de clientes no sistema (L)")
    print("5. Número médio de clientes na fila (Lq)")
    print("6. Tempo médio no sistema (W)")
    print("7. Tempo médio na fila (Wq)")
    print("8. Probabilidade de tempo de espera no sistema maior que t (P(W > t))")
    print("9. Probabilidade de tempo de espera na fila maior que t (P(Wq > t))")
    print("10. Sair")


def handle_mm1_queue(queue: MM1Queue):
    while True:
        print(f"\nParâmetros da fila:\n{queue.p}")

        display_menu()
        choice = int(input("Escolha uma opção: "))
        clear_screen()

        match choice:
            case 1:
                n = int(input("Digite o valor de n: "))
                result = queue.prob_n_clients_in_system(n)
                print(f"Probabilidade de {n} clientes no sistema (Pn): {result}")
            case 2:
                result = queue.prob_system_empty()
                print(f"Probabilidade de o sistema estar vazio (P0): {result}")
            case 3:
                result = queue.prob_system_busy()
                print(f"Probabilidade de o sistema estar ocupado (1 - P0): {result}")
            case 4:
                result = queue.avg_number_clients_in_system()
                print(f"Número médio de clientes no sistema (L): {result}")
            case 5:
                result = queue.avg_number_clients_in_queue()
                print(f"Número médio de clientes na fila (Lq): {result}")
            case 6:
                result = queue.avg_time_in_system_per_client()
                print(f"Tempo médio no sistema (W): {result}")
            case 7:
                result = queue.avg_time_in_queue_per_client()
                print(f"Tempo médio na fila (Wq): {result}")
            case 8:
                t = float(input("Digite o valor de t: "))
                result = queue.prob_wait_in_system_bigger_than(t)
                print(f"Probabilidade de tempo de espera no sistema maior que {t} (P(W > t)): {result}")
            case 9:
                t = float(input("Digite o valor de t: "))
                result = queue.prob_wait_in_queue_bigger_than(t)
                print(f"Probabilidade de tempo de espera na fila maior que {t} (P(Wq > t)): {result}")
            case 10:
                print("Saindo do menu MM1...")
                break
            case _:
                print("Opção inválida. Tente novamente.")

        input("Pressione Enter para continuar...")
        clear_screen()


def handle_mms_queue(queue: MMsQueue):
    while True:
        print(f"\nParâmetros da fila:\n{queue.p}")

        display_menu()
        choice = int(input("Escolha uma opção: "))
        clear_screen()

        match choice:
            case 1:
                n = int(input("Digite o valor de n: "))
                result = queue.prob_n_clients_in_system(n)
                print(f"Probabilidade de {n} clientes no sistema (Pn): {result}")
            case 2:
                result = queue.prob_zero_clients_in_system()
                print(f"Probabilidade de o sistema estar vazio (P0): {result}")
            case 3:
                print("Essa funcionalidade não está implementada para MMs.")
            case 4:
                result = queue.avg_number_clients_in_system()
                print(f"Número médio de clientes no sistema (L): {result}")
            case 5:
                result = queue.avg_number_clients_in_queue()
                print(f"Número médio de clientes na fila (Lq): {result}")
            case 6:
                result = queue.avg_time_in_system()
                print(f"Tempo médio no sistema (W): {result}")
            case 7:
                result = queue.avg_time_in_queue()
                print(f"Tempo médio na fila (Wq): {result}")
            case 8:
                t = float(input("Digite o valor de t: "))
                result = queue.prob_time_spent_in_system_bigger_than(t)
                print(f"Probabilidade de tempo de espera no sistema maior que {t} (P(W > t)): {result}")
            case 9:
                t = float(input("Digite o valor de t: "))
                result = queue.prob_time_spent_in_queue_bigger_than(t)
                print(f"Probabilidade de tempo de espera na fila maior que {t} (P(Wq > t)): {result}")
            case 10:
                print("Saindo do menu MMs...")
                break
            case _:
                print("Opção inválida. Tente novamente.")

        input("Pressione Enter para continuar...")
        clear_screen()


def run():
    print("Bem-vindo ao simulador de filas M/M/s!")
    params = get_queue_data()

    if params.s == 1:
        queue = MM1Queue(params)
        handle_mm1_queue(queue)
    else:
        queue = MMsQueue(params)
        handle_mms_queue(queue)