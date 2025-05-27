import queues.mg1.menu as menu_mg1
import queues.mms.menu as menu_mms
import queues.mmsn.menu as menu_mmsn

from utils.utils import clear_screen

def display_menu():
    print("Selecione o tipo de fila:")
    print("1. M/M/1")
    print("2. M/M/s")
    print("3. M/M/s/n")
    print("4. Sair")

def main():
    while True:
        display_menu()
        choice = input("Digite sua escolha (1-4): ")
        clear_screen()

        if choice == '1':
            menu_mg1.run()
        elif choice == '2':
            menu_mms.run()
        elif choice == '3':
            menu_mmsn.run()
        elif choice == '4':
            print("Saindo do programa.")
            break
        else:
            print("Escolha inválida. Tente novamente.")

        clear_screen()


if __name__ == "__main__":
    main()
