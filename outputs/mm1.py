from main import main
def show_menu(mm1):
    while True:
        print("Calculadora MM1")
        print("1: Probabilidade de o sistema estar ocupado ρ")
        print("2. Probabilidade de haver n clientes no sistema P(n)")
        print("3. Probabilidade de que o número de clientes no sistema seja superior a um valor r P(n > r)")
        print("4. Probabilidade de que sistema esteja ocioso P(n = 0)")
        print("6. Probabilidade do tempo de espera no sistema P(W > t)")
        print("7. Probabilidade do tempo de espera na fila P(Wq > t)")
        print("8. Tempo médio de espera no sistema W")
        print("9. Tempo médio de espera na fila Wq")
        print("10. Número médio de clientes no sistema L")
        print("11. Número médio de clientes na fila Lq")
        print("Pressione qualquer outra para sair.")
        option = int(input("Digite a opção desejada: "))
        match option:
            case 1:
                print(mm1.probability_system_busy())
            case 2:
                n = int(input("Digite o valor de n: "))
                print(mm1.probability_n_clients_in_system(n))
            case 3:
                r = int(input("Digite o valor de r: "))
                print(mm1.probability_n_clients_more_than_r(r))
                show_menu(mm1)
            case 4:
                print(mm1.probability_system_idle())
            case 5:
                print(mm1.probability_system_busy())
            case 6:
                t = int(input("Digite o valor do tempo: "))
                print(mm1.probability_time_spent_in_system(t))
            case 7:
                t = float(input("Digite o valor do tempo: "))
                print(mm1.probability_time_spent_in_queue(t))
            case 8:
                print(mm1.avg_time_spent_in_system_per_client())
            case 9:
                print(mm1.avg_time_spent_in_queue())
            case 10:
                print(mm1.avg_number_of_clients_in_system())
            case 11:
                print(mm1.avg_number_of_clients_in_queue())
            case _:
                main()