import queues.mg1.menu as menu_mg1
import queues.mms.menu as menu_mms
import queues.mmsn.menu as menu_mmsn
import queues.mmsk.menu as menu_mmsk
import queues.priority_model.with_interruption.menu as menu_priority_with_interruption
import queues.priority_model.without_interruption.menu as menu_priority_without_interruption

from utils.utils import clear_screen

def display_menu():
    print("Selecione o tipo de fila:")
    print("1. M/G/1")
    print("2. M/M/s")
    print("3. M/M/s/n")
    print("4. M/M/s/K")
    print("5. Prioridade sem interrupção")
    print("6. Prioridade com interrupção")
    print("7. Sair")

def main():
    while True:
        display_menu()
        choice = input("Digite sua escolha (1-5): ")
        clear_screen()

        if choice == '1':
            menu_mg1.run()
        elif choice == '2':
            menu_mms.run()
        elif choice == '3':
            menu_mmsn.run()
        elif choice == '4':
            menu_mmsk.run()
        elif choice == '5':
            menu_priority_without_interruption.run()
        elif choice == '6':
            menu_priority_with_interruption.run()
        elif choice == '7':
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Por favor, tente novamente.")

        clear_screen()


if __name__ == "__main__":
    main()
