from tkinter import simpledialog
class Params:
    def __init__(self, lmbd, avg, deviation):
        self.lmbd = lmbd
        self.avg = avg
        self.deviation = deviation

        self.mu = 1 / avg
        self.rho = lmbd / self.mu

    def __str__(self):
        return f"lambda (λ): {self.lmbd}, mu (μ): {self.mu}, rho (ρ): {self.rho}, média: {self.avg}, sigma(σ^2): {self.deviation}"

def get_queue_data():
    lmbd = simpledialog.askfloat("Parâmetro", "Digite o valor de lambda (λ):")
    avg = simpledialog.askfloat("Parâmetro", "Digite o valor da média:")
    deviation = simpledialog.askfloat("Parâmetro", "Digite o valor da variância: ")

    return Params(lmbd, avg, deviation)