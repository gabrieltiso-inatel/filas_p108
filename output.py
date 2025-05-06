from measures import MeasuresCalculator

def run_menu(calculator: MeasuresCalculator):
    print("\nEscolha uma opção:")
    print("1. Probabilidade de 0 clientes no sistema")
    print("2. Probabilidade de n clientes no sistema")
    print("3. Probabilidade de tempo gasto na fila")
    print("4. Probabilidade de tempo gasto no sistema")
    print("5. Número médio de clientes na fila")
    print("6. Número médio de clientes no sistema")
    print("7. Tempo médio gasto na fila")
    print("8. Tempo médio gasto no sistema")
    print("9. Sair")

    while True:
        choice = input("Digite o número da opção desejada: ").strip()

        if choice == "1":
            print("Probabilidade de 0 clientes no sistema:", calculator.probability_zero_clients_in_system())
        elif choice == "2":
            n = int(input("Digite o valor de n: "))
            print(f"Probabilidade de {n} clientes no sistema:", calculator.probability_n_clients_in_system(n))
        elif choice == "3":
            t = int(input("Digite o valor de t: "))
            print(f"Probabilidade de tempo gasto na fila maior que {t}:", calculator.probability_time_spent_in_queue(t))
        elif choice == "4":
            t = int(input("Digite o valor de t: "))
            print(f"Probabilidade de tempo gasto no sistema maior que {t}:", calculator.probability_time_spent_in_system(t))
        elif choice == "5":
            print("Número médio de clientes na fila:", calculator.avg_number_of_clients_in_queue())
        elif choice == "6":
            print("Número médio de clientes no sistema:", calculator.avg_number_of_clients_in_system())
        elif choice == "7":
            print("Tempo médio gasto na fila:", calculator.time_spent_in_queue())
        elif choice == "8":
            print("Tempo médio gasto no sistema:", calculator.time_spent_in_system())
        elif choice == "9":
            break
        else:
            print("Opção inválida. Tente novamente.")
