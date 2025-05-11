import math

from queues.mms.input import Params

class MMQueue:
    def __init__(self, params: Params):
        self.params = params

class MM1Queue(MMQueue):
    def __init__(self, params: Params):
        super().__init__(params)

    def prob_n_clients_in_system(self, n):
        return (1 - self.params.rho) * (self.params.rho ** n)
    
    def prob_number_clients_in_system_bigger_than(self, r):
        return (self.params.lambda_param / self.params.mu_param) ** (r + 1)
    
    def prob_system_empty(self):
        return (self.params.mu_param - self.params.lambda_param) / self.params.mu_param
    
    def prob_system_busy(self):
        return self.params.rho
    
    def prob_wait_in_system_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        return math.exp(-self.params.mu_param * (1 - self.params.rho) * t)
    
    def prob_wait_in_queue_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        return self.params.rho * self.prob_wait_in_system_bigger_than(t)
    
    def avg_number_clients_in_system(self):
        return self.params.lambda_param * self.avg_time_in_system()
    
    def avg_number_clients_in_queue(self):
        return self.params.lambda_param * self.avg_time_in_queue()
    
    def avg_time_in_system(self):
        return 1 / (self.params.mu_param - self.params.lambda_param)
    
    def avg_time_in_queue(self):
        return self.params.lambda_param / (self.params.mu_param * (self.params.mu_param - self.params.lambda_param))
    
class MMsQueue(MMQueue):
    def __init__(self, params: Params):
        super().__init__(params)

    def prob_zero_clients_in_system(self):
        summation = sum(((self.params.lambda_param / self.params.mu_param)**n / math.factorial(n)) for n in range(self.params.s_param))
        first_term = ((self.params.lambda_param / self.params.mu_param) ** self.params.s_param) / math.factorial(self.params.s_param)
        second_term = 1 / (1 - self.params.rho)

        return 1 / (summation + first_term * second_term)

    def prob_n_clients_in_system(self, n):
        if n < self.params.s_param:
            return ((self.params.lambda_param / self.params.mu_param)**n / math.factorial(n)) * self.prob_zero_clients_in_system()

        return ((self.params.lambda_param / self.params.mu_param)**n / (math.factorial(self.params.s_param) * self.params.s_param**(n - self.params.s_param))) * self.prob_zero_clients_in_system()
    
    def prob_time_spent_in_system_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"

        first_exp = math.exp(-self.params.mu_param * t)
        first_term = (self.prob_zero_clients_in_system() * ((self.params.lambda_param / self.params.mu_param) ** self.params.s_param)) / (math.factorial(self.params.s_param) * (1 - self.params.rho))
        second_term = (1 - math.exp(-self.params.mu_param * t * (self.params.s_param - 1 - (self.params.lambda_param / self.params.mu_param)))) / (self.params.s_param - 1 - (self.params.lambda_param / self.params.mu_param))

        return first_exp + (1 + first_term * second_term)
    
    def prob_time_spent_in_queue_bigger_than(self, t):
        assert t >= 0, "Tempo deve ser maior ou igual a zero"
        prob_time_in_queue_is_zero = sum(self.prob_n_clients_in_system(n) for n in range(self.params.s_param))

        return (1 - prob_time_in_queue_is_zero) * math.exp(-self.params.s_param * self.params.mu_param * (1 - self.params.rho) * t)
    
    def avg_number_clients_in_queue(self):
        nominator = (self.prob_zero_clients_in_system() * (self.params.lambda_param / self.params.mu_param)**self.params.s_param * self.params.rho)
        denominator = math.factorial(self.params.s_param) * (1 - self.params.rho)**2
        return nominator / denominator
    
    def avg_number_clients_in_system(self):
        return self.avg_number_clients_in_queue() + (self.params.lambda_param / self.params.mu_param)
    
    def avg_time_in_queue(self):
        return self.avg_number_clients_in_queue() / self.params.mu_param
    
    def avg_time_in_system(self):
        return self.avg_number_clients_in_system() / self.params.lambda_param