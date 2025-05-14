from math import factorial
from queues.mmsn.input import Params

class MMNQueue:
    def __init__(self, p: Params):
        self.p = p

# Giovani
class MM1NQueue(MMNQueue):
    def __init__(self, p: Params):
        super().__init__(p)
        self.rho = (p.n * p.lmbd) / p.mu

# Gabriel
class MMsNQueue(MMNQueue):
    def __init__(self, p: Params):
        super().__init__(p)
        self.first_summation_term = lambda n: ((factorial(self.p.n)) / (factorial(self.p.n - n) * factorial(n))) * ((self.p.lmbd / self.p.mu)**n)
        self.second_summation_term = lambda n: ((factorial(self.p.n)) / (factorial(self.p.n - n) * factorial(self.p.s) * (self.p.s**(n - self.p.s)))) * ((self.p.lmbd / self.p.mu)**n)

    def prob_zero_clients_in_system(self):
        return 1 / (sum(self.first_summation_term(n_val) for n_val in range(self.p.s)) + sum(self.second_summation_term(n_val) for n_val in range(self.p.s, self.p.n + 1)))
    
    def prob_n_clients_in_system(self, n: int):
        p0 = self.prob_zero_clients_in_system()
        if n <= self.p.s:
            return self.first_summation_term(n) * p0
        elif n >= self.p.s and n <= self.p.n:
            return self.second_summation_term(n) * p0
        elif n > self.p.n:
            return 0
        
    def avg_number_clients_in_system(self):
        return sum(n * self.prob_n_clients_in_system(n) for n in range(1, self.p.n + 1))
    
    def avg_number_clients_in_queue(self):
        return self.avg_number_clients_in_system() - (self.p.lmbd / self.p.mu)*(self.p.n - self.avg_number_clients_in_system())
    
    def avg_time_in_system(self):
        return self.avg_number_clients_in_system() / (self.p.lmbd * (self.p.n - self.avg_number_clients_in_system()))
    
    def avg_time_in_queue(self):
        return self.avg_number_clients_in_queue() / (self.p.lmbd * (self.p.n - self.avg_number_clients_in_system()))