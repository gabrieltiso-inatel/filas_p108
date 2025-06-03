class Params:
    def __init__(self, lmbds, mu, s, K):
        self.lmbds = lmbds
        self.mu = mu
        self.s = s
        self.K = K
        self.rho = lmbds / (s * mu)

    def __str__(self):
        return f"lambda (λ): {self.lmbds}, mu (μ): {self.mu}, s: {self.s}, K: {self.K}"

def get_queue_data():
    lmbds = float(input("Digite o valor de lambda: ")) 
    mu = float(input("Digite o valor de mu: "))
    s = int(input("Digite o valor de s: "))
    K = int(input("Digite o valor de K: "))

    return Params(lmbds, mu, s, K)