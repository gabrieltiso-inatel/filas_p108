class Params:
    def __init__(self, lambda_param, mu_param, s_param, n_param):
        self.lmbd = lambda_param
        self.mu = mu_param
        self.s = s_param
        self.n = n_param

    def __str__(self):
        return f"Lambda: {self.lmbd}, Mu: {self.mu}, S: {self.s}, N: {self.n}"

def get_queue_data():
    lambda_param = float(input("Digite o valore de lamda: ")) 
    mu_param = float(input("Digite o valore de mu: "))
    s_param = int(input("Digite o valore de s: "))
    n_param = int(input("Digite o valore de N "))

    return Params(lambda_param, mu_param, s_param, n_param)
