import os, platform

from typing import Dict, Any

def clear_screen():
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def show_menu(options: Dict[str, Any]):
    print("\nMenu de Opções:")
    for k, option in options.items():
        print(f"{k}. {option[0]}")
    print(f"{len(options)}. Sair")

def queue_loop(queue, options):
    while True:
        print(f"\nParâmetros da fila:\n{queue.p}")

        show_menu(options)
        choice = int(input("Escolha uma opção: "))
        clear_screen()

        if choice < 0 or choice > len(options):
            print("Opção inválida. Tente novamente.")
            continue

        if choice == len(options):
            print("Saindo do programa...")
            break

        fn = options[choice][1]
        print(f"Resultado: {fn()}")

        input("Pressione Enter para continuar...")
        clear_screen()