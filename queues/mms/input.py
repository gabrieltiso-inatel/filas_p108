class Params:
    def __init__(self, lambda_param, mu_param, s_param):
        self.lmbd = lambda_param
        self.mu = mu_param
        self.s = s_param
        self.rho = lambda_param / (s_param * mu_param)

    def __str__(self):
        return f"Lambda: {self.lmbd}\nMu: {self.mu}\nRho: {self.rho}\nS: {self.s}"

def get_queue_data():
    lambda_param = float(input("Digite o valore de lamda: ")) 
    mu_param = float(input("Digite o valore de mu: "))
    s_param = int(input("Digite o valore de s: "))

    return Params(lambda_param, mu_param, s_param)