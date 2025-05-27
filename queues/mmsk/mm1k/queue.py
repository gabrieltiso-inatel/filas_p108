import math
from dataclasses import dataclass

@dataclass
class Params:
    lmbd: float  # arrival rate λ
    mu: float    # service rate μ
    K: int       # system capacity (including the one in service)

class MM1KQueue:
    def __init__(self, p: Params):
        self.p = p
        self.rho = p.lmbd / p.mu

    def prob_zero_clients_in_system(self):
        """P₀"""
        if self.rho == 1:
            # equal‐rates case: P₀ = 1/(K+1)
            return 1 / (self.p.K + 1)
        # general case
        return (1 - self.rho) / (1 - self.rho**(self.p.K + 1))

    def prob_n_clients_in_system(self, n: int):
        """Pₙ for 0 ≤ n ≤ K"""
        P0 = self.prob_zero_clients_in_system()
        if 0 <= n <= self.p.K:
            return P0 * (self.rho**n)
        return 0.0

    def avg_number_clients_in_system(self):
        """L = E[# in system]"""
        K, ρ = self.p.K, self.rho
        P0 = self.prob_zero_clients_in_system()

        if ρ == 1:
            # L = K/2 when ρ=1
            return K / 2

        # L = ρ * (1 - (K+1)ρ^K + K ρ^(K+1)) / ((1 - ρ) * (1 - ρ^(K+1)))
        num = ρ * (1 - (K + 1) * ρ**K + K * ρ**(K + 1))
        den = (1 - ρ) * (1 - ρ**(K + 1))
        return num / den

    def avg_number_clients_in_queue(self):
        """Lq = E[# in queue] = L – (prob server busy)"""
        L = self.avg_number_clients_in_system()
        # server is busy iff ≥1 in system ⇒ P(busy) = 1 – P₀
        return L - (1 - self.prob_zero_clients_in_system())

    def avg_effective_arrival_rate(self):
        """λₑ = λ (1 – P_K)"""
        PK = self.prob_n_clients_in_system(self.p.K)
        return self.p.lmbd * (1 - PK)

    def avg_wait_time_in_system(self):
        """W = L / λₑ"""
        return self.avg_number_clients_in_system() / self.avg_effective_arrival_rate()

    def avg_wait_time_in_queue(self):
        """Wq = Lq / λₑ"""
        return self.avg_number_clients_in_queue() / self.avg_effective_arrival_rate()
