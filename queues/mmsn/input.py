class Params:
    def __init__(self, lmdb, mu, s, n):
        self.lmbd = lmdb
        self.mu = mu
        self.s = s
        self.n = n

    def __str__(self):
        return f"lambda (λ): {self.lmbd}, mu (μ): {self.mu}, s: {self.s}, n: {self.n}"

def get_queue_data():
    lmbd = float(input("Digite o valore de lamda: ")) 
    mu = float(input("Digite o valore de mu: "))
    s = int(input("Digite o valore de s: "))
    n = int(input("Digite o valore de N "))

    return Params(lmbd, mu, s, n)
