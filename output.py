def run_menu(calculator):
    print("\nEscolha uma opção:")
    print("1. Probabilidade de 0 clientes no sistema P(0)")
    print("2. Probabilidade de haver n clientes no sistema P(n)")
    print("3. Probabilidade do tempo de espera na fila P(Wq > t)")
    print("4. Probabilidade do tempo de espera no sistema P(W > t)")
    print("5. Número médio de clientes na fila Lq")
    print("6. Número médio de clientes no sistema L")
    print("7. Tempo médio de espera na fila Wq")
    print("8. Tempo médio de espera no sistema W")
    print("9. Probabilidade do sistema estar ocupado ρ")
    print("10.Probabilidade de que o número de clientes no sistema seja superior a um valor r P(n > r)")
    print("11. Probabilidade de que sistema esteja ocioso P(n = 0)")
    print("12. Sair")

    while True:
        choice = int(input("Digite o número da opção desejada: ").strip())
        match choice: 
            case 1:
                print("Probabilidade de 0 clientes no sistema:", calculator.probability_zero_clients_in_system())
            case 2:
                n = int(input("Digite o valor de n: "))
                print(f"Probabilidade de {n} clientes no sistema:", calculator.probability_n_clients_in_system(n))
            case 3:
                t = int(input("Digite o valor de t: "))
                print(f"Probabilidade de tempo gasto na fila maior que {t}:", calculator.probability_time_spent_in_queue(t))
            case 4:
                t = int(input("Digite o valor de t: "))
                print(f"Probabilidade de tempo gasto no sistema maior que {t}:", calculator.probability_time_spent_in_system(t))
            case 5:
                print("Número médio de clientes na fila:", calculator.avg_number_of_clients_in_queue())
            case 6:
                print("Número médio de clientes no sistema:", calculator.avg_number_of_clients_in_system())
            case 7:
                print("Tempo médio gasto na fila:", calculator.avg_time_spent_in_queue())
            case 8:
                print("Tempo médio gasto no sistema:", calculator.avg_time_spent_in_queue())
            case 9:
                print("Probabilidade do sistema estar ocupado: ", calculator.probability_system_busy())
            case 10:
                r = int(input("Digite o valor de r: "))
                print(f"Probabilidade P(n>{r}):", calculator.avg_number_of_clients_in_system())
            case 11:
                print("Probabilidade que o sistema esteja ocioso", calculator.probability_system_idle())
            case 12:
                break
            case _:
                print("Opção inválida. Tente novamente.")
