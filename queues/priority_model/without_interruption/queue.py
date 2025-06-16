from math import factorial
from queues.priority_model.without_interruption.input import Params

class PriorityModelWithoutInterruption:
    def __init__(self, p: Params):
        self.p = p
    
    def avg_waiting_time_in_system(self) -> list[float]:
        ret = []
        for i in range(self.p.n):
            r = self.p.lmbds[i] / self.p.mu
            summation1 = sum([(r**j) / factorial(j) for j in range(self.p.s)])

            term1 = factorial(self.p.s) * ((self.p.s*self.p.mu - self.p.lmbds[i]) / (r**self.p.s)) * summation1 + self.p.s*self.p.mu
            term2 = (1 - (sum(self.p.lmbds[:i]) / (self.p.s * self.p.mu)))
            term3 = (1 - (sum(self.p.lmbds[:i + 1]) / (self.p.s * self.p.mu)))

            ret.append((1 / (term1 * term2 * term3)) + (1 / self.p.mu))

        return ret

    def avg_waiting_time_in_queue(self) -> list[float]:
        W = self.avg_waiting_time_in_system()
        return [W[i] - (1 / self.p.mu) for i in range(self.p.n)]

    def avg_clients_in_system(self) -> list[float]:
        W = self.avg_waiting_time_in_system()
        return [self.p.lmbds[i] * W[i] for i in range(self.p.n)]

    def avg_clients_in_queue(self) -> list[float]:
        L = self.avg_clients_in_system()
        return [L[i] - (self.p.lmbds[i] / self.p.mu) for i in range(self.p.n)]
