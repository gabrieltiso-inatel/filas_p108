import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import queues.mg1.menu as menu_mg1
import queues.mms.menu as menu_mms
import queues.mmsn.menu as menu_mmsn
import queues.mmsk.menu as menu_mmsk
import queues.priority_model.with_interruption.menu as menu_priority_with_interruption

class QueueSimulatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Filas")
        self.root.geometry("600x500")
        
        self.main_frame = ttk.Frame(root, padding="10")
        self.main_frame.pack(fill=tk.BOTH, expand=True)
        
        self.title_label = ttk.Label(self.main_frame, text="Simulador de Filas", font=("Arial", 16, "bold"))
        self.title_label.pack(pady=10)
        
        self.select_label = ttk.Label(self.main_frame, text="Selecione o tipo de fila:")
        self.select_label.pack(anchor=tk.W, pady=5)

        self.radio_frame = ttk.Frame(self.main_frame)
        self.radio_frame.pack(fill=tk.X, pady=5)
        
        self.queue_type = tk.StringVar(value="1")

        self.radio_mg1 = ttk.Radiobutton(self.radio_frame, text="M/G/1", variable=self.queue_type, value="1")
        self.radio_mg1.pack(anchor=tk.W, pady=2)

        self.radio_mms = ttk.Radiobutton(self.radio_frame, text="M/M/s", variable=self.queue_type, value="2")
        self.radio_mms.pack(anchor=tk.W, pady=2)

        self.radio_mmsn = ttk.Radiobutton(self.radio_frame, text="M/M/s/n", variable=self.queue_type, value="3")
        self.radio_mmsn.pack(anchor=tk.W, pady=2)

        self.radio_mmsk = ttk.Radiobutton(self.radio_frame, text="M/M/s/K", variable=self.queue_type, value="4")
        self.radio_mmsk.pack(anchor=tk.W, pady=2)
        
        self.radio_priority = ttk.Radiobutton(self.radio_frame, text="Prioridade com interrupção", variable=self.queue_type, value="6")
        self.radio_priority.pack(anchor=tk.W, pady=2)

        self.button_frame = ttk.Frame(self.main_frame)
        self.button_frame.pack(pady=10)
        
        self.execute_button = ttk.Button(self.button_frame, text="Configurar Fila", command=self.configure_queue)
        self.execute_button.pack(side=tk.LEFT, padx=5)
        
        self.exit_button = ttk.Button(self.button_frame, text="Sair", command=self.root.destroy)
        self.exit_button.pack(side=tk.LEFT, padx=5)
        
        self.result_frame = ttk.LabelFrame(self.main_frame, text="Parâmetros e Resultados", padding="10")
        self.result_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        
        self.params_label = ttk.Label(self.result_frame, text="Nenhuma fila configurada")
        self.params_label.pack(anchor=tk.W, pady=5)
        
        self.methods_frame = ttk.Frame(self.result_frame)
        self.methods_frame.pack(fill=tk.BOTH, expand=True)
        
        self.current_queue = None
        self.current_methods = None
        self.method_buttons = []

    def configure_queue(self):
        choice = self.queue_type.get()
        
        for button in self.method_buttons:
            button.destroy()
        self.method_buttons = []
        
        if choice == '1':
            menu_mg1.run()
        elif choice == '2':
            menu_mms.run()
        elif choice == '3':
            menu_mmsn.run()
        elif choice == '4':
            menu_mmsk.run()
        elif choice == '5':
            print("Opção 5 selecionada.")
        elif choice == '6':
            menu_priority_with_interruption.run()
        elif choice == '7':
            print("Saindo do programa.")
    
    def update_params_display(self):
        if hasattr(self.current_queue, 'p'):
            self.params_label.config(text=f"Parâmetros da fila:\n{self.current_queue.p}")
        else:

            params_text = "Parâmetros da fila:\n"
            if hasattr(self.current_queue, 'lmbd'):
                params_text += f"lambda (λ): {self.current_queue.lmbd}, "
            if hasattr(self.current_queue, 'mu'):
                params_text += f"mu (μ): {self.current_queue.mu}, "
            if hasattr(self.current_queue, 's'):
                params_text += f"s: {self.current_queue.s}, "
            if hasattr(self.current_queue, 'K'):
                params_text += f"K: {self.current_queue.K}"
            self.params_label.config(text=params_text)
    
    def create_method_buttons(self):
        if self.current_methods:
            methods_label = ttk.Label(self.methods_frame, text="Métodos disponíveis:", font=("Arial", 10, "bold"))
            methods_label.pack(anchor=tk.W, pady=(10, 5))
            self.method_buttons.append(methods_label)
            
            for key, (name, method) in self.current_methods.items():
                button = ttk.Button(
                    self.methods_frame, 
                    text=name,
                    command=lambda m=method, n=name: self.execute_method(m, n)
                )
                button.pack(fill=tk.X, pady=2)
                self.method_buttons.append(button)
    
    def execute_method(self, method, name):
        try:
            result = method()
            messagebox.showinfo("Resultado", f"{name}:\n{result:.6f}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar método: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = QueueSimulatorApp(root)
    root.mainloop()