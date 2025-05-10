class Params:
    def __init__(self, lambda_param, mu_param, s_param, n_param):
        self.lambda_param = lambda_param
        self.mu_param = mu_param
        self.s_param = s_param
        self.n_param = n_param
        self.rho = lambda_param / mu_param

    def __str__(self):
        return f"Lambda: {self.lambda_param}, Mu: {self.mu_param}, S: {self.s_param}, N: {self.n_param}"

def get_queue_data():
    lambda_param = float(input("Digite o valore de lamda: ")) 
    mu_param = float(input("Digite o valore de mu: "))
    s_param = int(input("Digite o valore de s: "))
    n_param = int(input("Digite o valore de N "))

    return Params(lambda_param, mu_param, s_param, n_param)