import os, platform
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Callable

def clear_screen():
    
    if platform.system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')

def show_menu_tkinter(parent: tk.Widget, options: Dict[int, Any], callback: Callable):
    """
    Cria botões para cada opção do menu em um widget pai
    
    Args:
        parent: Widget pai onde os botões serão criados
        options: Dicionário de opções (mesmo formato do show_menu original)
        callback: Função a ser chamada quando um botão for clicado, recebe o índice da opção
    """
    
    for widget in parent.winfo_children():
        widget.destroy()
        
    
    title_label = ttk.Label(parent, text="Menu de Opções:", font=("Arial", 10, "bold"))
    title_label.pack(anchor=tk.W, pady=(10, 5))
    
    
    for k, option in options.items():
        button = ttk.Button(
            parent,
            text=option[0],
            command=lambda idx=k: callback(idx)
        )
        button.pack(fill=tk.X, pady=2)
    
    
    exit_button = ttk.Button(
        parent,
        text="Sair",
        command=lambda: callback(len(options))
    )
    exit_button.pack(fill=tk.X, pady=2)

def queue_loop_tkinter(root: tk.Tk, queue, options: Dict[int, Any]):
    """
    Versão Tkinter do queue_loop
    
    Args:
        root: Janela principal do Tkinter
        queue: Objeto da fila
        options: Dicionário de opções de métodos
    """
    
    main_frame = ttk.Frame(root, padding="10")
    main_frame.pack(fill=tk.BOTH, expand=True)
    
    
    params_frame = ttk.LabelFrame(main_frame, text="Parâmetros da Fila", padding="10")
    params_frame.pack(fill=tk.X, pady=10)
    
    
    if hasattr(queue, 'p'):
        params_text = str(queue.p)
    else:
        
        params_text = ""
        if hasattr(queue, 'lmbd'):
            params_text += f"lambda (λ): {queue.lmbd}, "
        if hasattr(queue, 'mu'):
            params_text += f"mu (μ): {queue.mu}, "
        if hasattr(queue, 's'):
            params_text += f"s: {queue.s}, "
        if hasattr(queue, 'K'):
            params_text += f"K: {queue.K}"
    
    params_label = ttk.Label(params_frame, text=params_text, wraplength=400)
    params_label.pack(anchor=tk.W, pady=5)
    
    
    menu_frame = ttk.LabelFrame(main_frame, text="Métodos Disponíveis", padding="10")
    menu_frame.pack(fill=tk.BOTH, expand=True, pady=10)
    
    
    result_frame = ttk.LabelFrame(main_frame, text="Resultado", padding="10")
    result_frame.pack(fill=tk.X, pady=10)
    
    result_label = ttk.Label(result_frame, text="Selecione um método para ver o resultado", wraplength=400)
    result_label.pack(anchor=tk.W, pady=5)
    
    
    def handle_option(choice):
        if choice < 0 or choice > len(options):
            messagebox.showwarning("Aviso", "Opção inválida. Tente novamente.")
            return
            
        if choice == len(options):
            if messagebox.askyesno("Sair", "Deseja realmente sair?"):
                root.destroy()
            return
            
        try:
            fn = options[choice][1]
            result = fn()
            result_label.config(text=f"Resultado: {result:.6f}")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao executar método: {str(e)}")
    
    show_menu_tkinter(menu_frame, options, handle_option)

def create_queue_window(queue, options, title="Simulador de Filas"):
    """
    Cria uma janela Tkinter para uma fila específica
    
    Args:
        queue: Objeto da fila
        options: Dicionário de opções de métodos
        title: Título da janela
    """
    window = tk.Toplevel()
    window.title(title)
    window.geometry("500x600")
    
    queue_loop_tkinter(window, queue, options)
    
    return window
