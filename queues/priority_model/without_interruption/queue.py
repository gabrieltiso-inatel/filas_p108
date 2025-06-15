from math import factorial
from queues.priority_model.with_interruption.input import Params


class PriorityModelWithoutInterruption:
    """
    Calculates average waiting times and client counts for a non-preemptive priority queue without interruptions.
    """
    def __init__(self, p: Params):
        self.p = p

    def avg_waiting_time_in_system(self) -> list[float]:
        """
        Returns a list of average times each priority class spends in the system (waiting + service).
        """
        p = self.p
        r = p.total_lambda / p.mu
        sum_one = sum(r**j / factorial(j) for j in range(p.s))
        term_A = (factorial(p.s) * (p.s * p.mu - p.total_lambda) / (r**p.s) * sum_one) + (p.s * p.mu)

        waiting_times = []
        for i in range(p.n):
            raw_sum_k = sum(p.lmbds[:i])
            raw_sum_k1 = sum(p.lmbds[:i+1])

            term_B = 1 - (raw_sum_k1 / (p.s * p.mu))
            term_C = 1 - (raw_sum_k / (p.s * p.mu))

            denom = (term_A * term_B * term_C) + (1 / p.mu)
            waiting_times.append(1 / denom)

        return waiting_times

    def avg_waiting_time_in_queue(self) -> list[float]:
        """
        Returns a list of average times each priority class spends waiting (excluding service).
        """
        W = self.avg_waiting_time_in_system()
        return [w - (1 / self.p.mu) for w in W]

    def avg_clients_in_system(self) -> list[float]:
        """
        Returns a list of average number of clients in system for each priority class.
        """
        W = self.avg_waiting_time_in_system()
        return [sum(self.p.lmbds[:i+1]) * W[i] for i in range(self.p.n)]

    def avg_clients_in_queue(self) -> list[float]:
        """
        Returns a list of average number of clients waiting in queue for each priority class.
        """
        L = self.avg_clients_in_system()
        return [L[i] - (sum(self.p.lmbds[:i+1]) / self.p.mu) for i in range(self.p.n)]
