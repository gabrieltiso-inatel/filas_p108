import math

from queues.mms.input import Params

class MMQueue:
    def __init__(self, p: Params):
        self.p = p

class MM1Queue(MMQueue):
    def __init__(self, params: Params):
        super().__init__(params)

    def prob_n_clients_in_system(self, n):
        return (1 - self.p.rho) * (self.p.rho**n)
    
    def prob_number_clients_in_system_bigger_than(self, r):
        return (self.p.lmbd / self.p.mu)**(r + 1)
    
    def prob_system_empty(self):
        return (self.p.mu - self.p.lmbd) / self.p.mu
    
    def prob_system_busy(self):
        return self.p.rho
    
    def prob_wait_in_system_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        return math.exp(-self.p.mu * (1 - self.p.rho) * t)
    
    def prob_wait_in_queue_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        return self.p.rho * self.prob_wait_in_system_bigger_than(t)
    
    def avg_number_clients_in_system(self):
        return self.p.lmbd / (self.p.mu - self.p.lmbd)
    
    def avg_number_clients_in_queue(self):
        return (self.p.lmbd**2) / (self.p.mu * (self.p.mu - self.p.lmbd))
    
    def avg_time_in_system_per_client(self):
        return 1 / (self.p.mu - self.p.lmbd)
    
    def avg_time_in_queue_per_client(self):
        return self.p.lmbd / (self.p.mu * (self.p.mu - self.p.lmbd))
    
class MMsQueue(MMQueue):
    def __init__(self, params: Params):
        super().__init__(params)

    def prob_zero_clients_in_system(self):
        summation = sum(((self.p.lmbd / self.p.mu)**n / math.factorial(n)) for n in range(self.p.s))
        first_term = ((self.p.lmbd / self.p.mu) ** self.p.s) / math.factorial(self.p.s)
        second_term = 1 / (1 - self.p.rho)

        return 1 / (summation + first_term * second_term)

    def prob_n_clients_in_system(self, n):
        if n < self.p.s:
            return ((self.p.lmbd / self.p.mu)**n / math.factorial(n)) * self.prob_zero_clients_in_system()
        return ((self.p.lmbd / self.p.mu)**n / ((math.factorial(self.p.s) * self.p.s**(n - self.p.s)) * self.prob_zero_clients_in_system()))
    
    def prob_time_spent_in_system_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"

        first_exp = math.exp(-self.p.mu * t)
        first_term = (self.prob_zero_clients_in_system() * ((self.p.lmbd / self.p.mu) ** self.p.s)) / (math.factorial(self.p.s) * (1 - self.p.rho))
        second_term = (1 - math.exp(-self.p.mu * t * (self.p.s - 1 - (self.p.lmbd / self.p.mu)))) / (self.p.s - 1 - (self.p.lmbd / self.p.mu))

        return first_exp * (1 + first_term * second_term)
    
    def prob_time_spent_in_queue_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        prob_time_in_queue_is_zero = sum(self.prob_n_clients_in_system(n) for n in range(self.p.s))

        return (1 - prob_time_in_queue_is_zero) * math.exp(-self.p.s * self.p.mu * (1 - self.p.rho) * t)
    
    def avg_number_clients_in_queue(self):
        nominator = (self.prob_zero_clients_in_system() * ((self.p.lmbd / self.p.mu)**self.p.s) * self.p.rho)
        denominator = math.factorial(self.p.s) * (1 - self.p.rho)**2
        return nominator / denominator
    
    def avg_number_clients_in_system(self):
        return self.avg_number_clients_in_queue() + (self.p.lmbd / self.p.mu)
    
    def avg_time_in_queue(self):
        return self.avg_number_clients_in_queue() / self.p.lmbd
    
    def avg_time_in_system(self):
        return self.avg_number_clients_in_system() / self.p.lmbd
