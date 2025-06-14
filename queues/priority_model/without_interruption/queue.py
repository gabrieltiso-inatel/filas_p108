from math import factorial
from queues.priority_model.with_interruption.input import Params

class PriorityModelWithoutInterruption:
    def __init__(self, p: Params):
        self.p = p

    def avg_waiting_time_in_system(self):
        r = self.p.total_lambda / self.p.mu
        sum_one = sum((r**j) / factorial(j) for j in range(self.p.s))
        term_A = factorial(self.p.s) * ((self.p.s * self.p.mu - self.p.total_lambda) / (r**self.p.s)) * sum_one + self.p.s * self.p.mu
        sum_k = 0
        sum_k_1 = 0
        for i in range(self.p.n):
            sum_k = sum(self.p.lmbds[:i]) / (self.p.s * self.p.mu)
            sum_k_1 = sum(self.p.lmbds[:i+1]) / (self.p.s * self.p.mu)
        term_B = 1 - (sum_k_1 / (self.p.s * self.p.mu))
        term_C = 1 - (sum_k / (self.p.s * self.p.mu))
        den = (term_A * term_B * term_C) + (1 / self.p.mu)
        result = 1 / den
        return result
    
    def avg_waiting_time_in_queue(self):
        avg_wait_in_system_arr = self.avg_waiting_time_in_system()
        avg_wait_in_queue_arr = []

        for i in range(self.p.n):
            result = avg_wait_in_system_arr[i] - (1 / self.p.mu)
            avg_wait_in_queue_arr.append(result)

        return avg_wait_in_queue_arr
    
    def avg_clients_in_system(self):
        avg_wait_in_system_arr = self.avg_waiting_time_in_system()
        avg_clients_in_system_arr = []
        for i in range(self.p.n):
            result = sum(self.p.lmbds[:i+1]) * avg_wait_in_system_arr[i]
            avg_clients_in_system_arr.append(result)

        return avg_clients_in_system_arr
    
    def avg_clients_in_queue(self):
        avg_clients_in_system_arr = self.avg_clients_in_system()
        avg_clients_in_queue_arr = []
        for i in range(self.p.n):
            result = avg_clients_in_system_arr[i] - (sum(self.p.lmbds[:i+1]) / self.p.mu)
            avg_clients_in_queue_arr.append(result)

        return avg_clients_in_queue_arr
