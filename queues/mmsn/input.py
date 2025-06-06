from tkinter import simpledialog
class Params:
    def __init__(self, lmdb, mu, s, n):
        self.lmbd = lmdb
        self.mu = mu
        self.s = s
        self.n = n

    def __str__(self):
        return f"lambda (λ): {self.lmbd}, mu (μ): {self.mu}, s: {self.s}, n: {self.n}"

def get_queue_data():
    lmbd = simpledialog.askfloat("Parâmetro", "Digite o valor de lambda (λ):")
    mu = simpledialog.askfloat("Parâmetro", "Digite o valor de mu:")
    s = simpledialog.askinteger("Parâmetro", "Digite o valor de s: ")
    n = simpledialog.askinteger("Parâmetro", "Digite o valor de N ")

    return Params(lmbd, mu, s, n)
