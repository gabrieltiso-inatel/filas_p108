from tkinter import simpledialog
class Params:
    def __init__(self, lmbd, mu, s):
        self.lmbd = lmbd
        self.mu = mu
        self.s = s
        self.rho = lmbd / (s * mu)

    def __str__(self):
        return f"lambda (λ): {self.lmbd}, mu (μ): {self.mu}, s: {self.s}, rho (ρ): {self.rho}"

def get_queue_data():
    lmbd = simpledialog.askfloat("Parâmetro", "Digite o valor de lambda (λ):")
    mu = simpledialog.askfloat("Parâmetro", "Digite o valor de mu: ")
    s = simpledialog.askinteger("Parâmetro", "Digite o valor de s: ")

    return Params(lmbd, mu, s)