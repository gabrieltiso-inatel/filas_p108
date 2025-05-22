class Params:
    def __init__(self, lmbd, mu, s):
        self.lmbd = lmbd
        self.mu = mu
        self.s = s
        self.rho = lmbd / (s * mu)

    def __str__(self):
        return f"lambda (λ): {self.lmbd}, mu (μ): {self.mu}, s: {self.s}, rho (ρ): {self.rho}"

def get_queue_data():
    mu = float(input("Digite o valore de lamda: ")) 
    mu = float(input("Digite o valore de mu: "))
    s = int(input("Digite o valore de s: "))

    return Params(mu, mu, s)