from math import factorial
from queues.priority_model.with_interruption.input import Params


class PriorityModelWithoutInterruption:
    """
    Calculates average waiting times and client counts for a non-preemptive priority queue without interruptions.
    """
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
        """
        Returns a list of average times each priority class spends waiting (excluding service).
        """
        W = self.avg_waiting_time_in_system()
        return [W[i] - (1 / self.p.mu) for i in range(self.p.n)]

    def avg_clients_in_system(self) -> list[float]:
        """
        Returns a list of average number of clients in system for each priority class.
        """
        W = self.avg_waiting_time_in_system()
        return [self.p.lmbds[i] * W[i] for i in range(self.p.n)]

    def avg_clients_in_queue(self) -> list[float]:
        """
        Returns a list of average number of clients waiting in queue for each priority class.
        """
        Wq = self.avg_waiting_time_in_queue()
        return [self.p.lmbds[i] * Wq[i] for i in range(self.p.n)]
