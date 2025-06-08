from tkinter import simpledialog, messagebox
class Params:
    def __init__(self, n, lmbds, mu, s, total_lambda):
        self.s = s
        self.mu = mu
        self.total_lambda = total_lambda
        self.n = n
        self.lmbds = lmbds  
        self.rho = self.total_lambda / (self.s * self.mu)

    def __str__(self):
        return f"n: {self.n}, lambda por prioridade: {self.lmbds}, mu (μ): {self.mu}, s: {self.s}, lambda total: {self.total_lambda}, rho (ρ): {self.rho}"

def get_queue_data():
    mu = simpledialog.askfloat("Parâmetro", "Digite o valor de mu: ")
    total_lambda = simpledialog.askfloat("Parâmetro", "Digite o valor de lambda total: ")
    s = simpledialog.askinteger("Parâmetro", "Digite o valor de s: ")
    n = simpledialog.askinteger("Parâmetro", "Digite o valor de N: ")
    percentages = []
    for i in range(n):
        percentages.append(simpledialog.askfloat("Parâmetro", f"Digite a porcentagem de lambda p{i+1}:"))
        
    lmbds = [total_lambda * p for p in percentages]

    if sum(lmbds) != total_lambda:
        raise ValueError("A soma das porcentagens deve ser igual a lambda total.")
    
    return Params(n, lmbds, mu, s, total_lambda)