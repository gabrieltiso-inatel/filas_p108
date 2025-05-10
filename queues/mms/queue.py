import math

class MMQueue:
    def __init__(self, params):
        self.params = params

class MM1Queue(MMQueue):
    def __init__(self, params):
        super().__init__(params)

    def prob_n_clients_in_system(self, n):
        return (1 - self.params.rho) * (self.params.rho ** n)
    
    def prob_number_clients_in_system_bigger_than(self, n, r):
        return (self.params.lambda_param / self.params.mu_param) ** (r + 1)
    
    def prob_system_empty(self):
        return (self.params.mu_param - self.params.lambda_param) / self.params.mu_param
    
    def prob_system_busy(self):
        return self.params.rho
    
    def prob_wait_in_system_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        return math.exp(-self.params.mu_param * (1 - self.params.rho_param) * t)
    
    def prob_wait_in_queue_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        return self.params.rho * self.prob_wait_in_queue_bigger_than(t)
    
    def avg_number_clients_in_system(self):
        return self.params.lambda_param / (self.params.mu_param - self.params.lambda_param)
    
    def avg_number_clients_in_queue(self):
        return self.params.rho * self.avg_number_clients_in_system()
    
    def avg_time_in_system(self):
        return 1 / (self.params.mu_param - self.params.lambda_param)
    
    def avg_time_in_queue(self):
        return self.rho * self.avg_time_in_system()
    
class MMSQueue(MMQueue):
    def __init__(self, params, s):
        super().__init__(params)
        self.s = s

    def prob_zero_clients_in_system(self):
        sum_terms = sum((self.params.rho ** n) / math.factorial(n) for n in range(self.s))
        last_term = ((self.params.rho ** self.s) / (math.factorial(self.s) * (1 - (self.params.lambda_param / (self.s * self.params.mu_param)))))

        denominator = sum_terms + last_term
        return 1 / denominator

    def prob_n_clients_in_system(self, n):
        if n < self.s:
            return ((self.params.rho ** n) / math.factorial(n)) * self.prob_zero_clients_in_system()

        return ((self.params.rho ** n) / (math.factorial(self.s) * (self.s ** (n - self.s)))) * self.prob_zero_clients_in_system()
    
    def prob_time_spent_in_system_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"

        first_exp = math.exp(-self.params.mu_param * t)
        first_term = (self.prob_zero_clients_in_system() * (self.params.rho ** self.s)) / (math.factorial(self.s) * (1 - self.params.rho))
        second_term = (1 - math.exp(-self.params.mu_param * t * (self.s - 1 - self.params.rho))) / (self.s - 1 - self.params.rho)

        return first_exp + (1 + first_term * second_term)
    
    def prob_time_spent_in_queue_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        prob_time_in_queue_is_zero = sum(self.prob_n_clients_in_system(n) for n in range(self.s))

        return (1 - prob_time_in_queue_is_zero) * math.exp(-self.s * self.params.mu_param * (1 - self.params.rho) * t)
    
    def avg_number_clients_in_queue(self):
        return (self.prob_zero_clients_in_system() * (self.params.rho ** self.s)) / (math.factorial(self.s) * ((1 - self.params.rho)**2))
    
    def avg_number_clients_in_system(self):
        return self.avg_number_clients_in_queue() + self.params.rho
    
    def avg_time_in_queue(self):
        return self.avg_number_clients_in_queue() / self.params.mu_param
    
    def avg_time_in_system(self):
        return self.avg_time_in_queue() + (1 / self.params.mu_param)
    