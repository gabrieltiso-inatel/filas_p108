import math

from queues.mmsk.input import Params

class MMSK:
    def __init__(self, p: Params):
        self.p = p

class MM1KQueue(MMSK):
    def __init__(self, params: Params):
        super().__init__(params)

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
    
    def prob_system_busy(self):
        return 1 - self.prob_zero_clients_in_system()

class MMSKQueue(MMSK):
    def __init__(self, params: Params):
        super().__init__(params)

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