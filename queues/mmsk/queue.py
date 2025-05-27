import math

from dataclasses import dataclass

@dataclass
class Params:
    lmbd: float  # Taxa de chegada (λ)
    mu: float    # Taxa de atendimento por servidor (μ)
    s: int       # Número de servidores
    K: int       # Capacidade máxima do sistema


class MMSKQueue:
    def __init__(self, p: Params):
        self.p = p
        self.rho = p.lmbd / (p.s * p.mu)

    def prob_zero_clients_in_system(self):
        sum1 = sum(
            (self.p.lmbd / self.p.mu) ** n / math.factorial(n)
            for n in range(self.p.s + 1)
        )
        sum2 = ((self.p.lmbd / self.p.mu) ** self.p.s) / math.factorial(self.p.s)
        sum3 = sum(
            (self.p.lmbd / (self.p.s * self.p.mu)) ** (n - self.p.s)
            for n in range(self.p.s + 1, self.p.K + 1)
        )

        P0 = 1 / (sum1 + sum2 * sum3)
        return P0

    def prob_n_clients_in_system(self, n):
        P0 = self.prob_zero_clients_in_system()
        if n <= self.p.s:
            return ((self.p.lmbd / self.p.mu) ** n) / math.factorial(n) * P0
        elif self.p.s < n <= self.p.K:
            return ((self.p.lmbd / self.p.mu) ** n) / (
                math.factorial(self.p.s) * (self.p.s ** (n - self.p.s))
            ) * P0
        else:
            return 0

    def avg_number_clients_in_queue(self):
        P0 = self.prob_zero_clients_in_system()
        numerator = (
            P0
            * ((self.p.lmbd / self.p.mu) ** self.p.s)
            * self.rho
            * (
                1
                - self.rho ** (self.p.K - self.p.s)
                - (self.p.K - self.p.s) * self.rho ** (self.p.K - self.p.s) * (1 - self.rho)
            )
        )
        denominator = math.factorial(self.p.s) * (1 - self.rho) ** 2

        return numerator / denominator

    def avg_number_clients_in_system(self):
        Lq = self.avg_number_clients_in_queue()
        Pn_sum = sum(
            n * self.prob_n_clients_in_system(n)
            for n in range(self.p.s)
        )
        return Lq + self.p.s * (1 - sum(self.prob_n_clients_in_system(n) for n in range(self.p.s))) + Pn_sum

    def avg_effective_arrival_rate(self):
        PK = self.prob_n_clients_in_system(self.p.K)
        return self.p.lmbd * (1 - PK)

    def avg_wait_time_in_queue(self):
        return self.avg_number_clients_in_queue() / self.avg_effective_arrival_rate()

    def avg_wait_time_in_system(self):
        return self.avg_number_clients_in_system() / self.avg_effective_arrival_rate()