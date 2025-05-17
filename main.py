from queues.mmsn import menu_mm1n

def main():
    print("Bem-vindo ao simulador!")
    print("1. M/M/s/N")
    print("7. Sair")
    choice = int(input("Digite o número da opção desejada: "))
    match choice:
        case 1:
            menu_mm1n.run()
        case 7:
            exit()
        case _:
            print("Opção inválida. Tente novamente.")
            main()

if __name__ == "__main__":
    main()
