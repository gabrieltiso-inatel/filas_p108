from math import factorial
from queues.mmsn.input import Params

class MMNQueue:
    def __init__(self, p: Params):
        self.n = p.n
        self.lmbd = p.lmbd
        self.mu = p.mu
        self.p = p

class MM1NQueue(MMNQueue):
    def __init__(self, p: Params):
        super().__init__(p)
        self.rho = (p.n * p.lmbd) / p.mu
        
    def prob_zero_clients_in_system(self): # P0
        sum = 0
        for i in range(self.n):
            term_one = factorial(self.n)/factorial(self.n - i)
            term_two = (self.lmbd / self.mu)**i
            sum += term_one * term_two
        return 1 / sum
    
    def prob_n_clients_in_system(self, n: int): # Pn
        p0 = self.prob_zero_clients_in_system()
        term_one = factorial(self.n)/(factorial(self.n - n))
        term_two = (self.lmbd / self.mu)**n
        return term_one * term_two * p0
    
    def avg_number_clients_in_queue(self):
        term_one = (self.lmbd + self.mu)/(self.lmbd)
        term_two = (1 - self.prob_zero_clients_in_system())
        lq = self.n - (term_one*term_two)
        return lq
    
    def avg_number_clients_in_system(self):
        term_one = (self.mu/self.lmbd)
        term_two = (1 - self.prob_zero_clients_in_system())
        term_three = (term_one * term_two)
        l = self.n - term_three
        return l
    
    def avg_lambda(self):
        return self.lmbd * (self.n - self.avg_number_clients_in_system())
    
    def avg_waiting_time_in_queue(self):
        lq = self.avg_number_clients_in_queue()
        avg_lambda = self.avg_lambda()
        wq = lq / avg_lambda
        return wq
    
    def avg_time_in_system(self):
        l = self.avg_number_clients_in_system()
        avg_lambda = self.avg_lambda()
        W = l / avg_lambda 
        return W
            
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