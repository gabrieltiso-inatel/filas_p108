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
    mu = float(input("Digite o valor de mu: "))
    total_lambda = float(input("Digite o valor de lambda total: "))
    s = int(input("Digite o valor de s: "))
    n = int(input("Digite o valor de N: "))

    percentages = input("Digite as porcentagens de lambda separadas por vírgula (ex: 0.1,0.2,0.3): ")
    lmbds = [total_lambda * float(p.strip()) for p in percentages.split(",")]

    if sum(lmbds) != total_lambda:
        raise ValueError("A soma das porcentagens deve ser igual a lambda total.")
    
    return Params(n, lmbds, mu, s, total_lambda)