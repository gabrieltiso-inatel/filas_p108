from math import factorial
from queues.priority_model.with_interruption.input import Params

class PriorityModelWithInterruptionQueueOneServer:
    def __init__(self, p: Params):
        self.p = p

    def avg_waiting_time_in_system(self):
        avg_wait_in_system_arr = [] 
        for i in range(self.p.n):
            nominator = (1 / self.p.mu)

            summation1 = sum(self.p.lmbds[:i]) / (self.p.s * self.p.mu)
            summation2 = sum(self.p.lmbds[:i+1]) / (self.p.s * self.p.mu)

            term1 = (1 - summation1)
            term2 = (1 - summation2)

            result = nominator / (term1 * term2)
            avg_wait_in_system_arr.append(result)

        return avg_wait_in_system_arr
    
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

class PriorityModelWithInterruptionQueueWithParamsMultipleServers:
    def __init__(self, p: Params):
        self.p = p

    def avg_waiting_time_in_system(self):
        avg_waiting_time_in_system_arr = []
        for i in range(self.p.n):
            avg_waiting_time_in_system_arr.append(self.calculate_average_waiting_time_in_system(i))            
        #     if i == 0:
        #         result = self.avg_clients_in_system()[i] / self.p.lmbds[i]
        #         avg_waiting_time_in_system_arr.append(result)
        #         continue

        #     result =
        return avg_waiting_time_in_system_arr

    def avg_waiting_time_in_queue(self):
        avg_waiting_time_in_system_arr = self.avg_waiting_time_in_system()
        avg_waiting_time_in_queue_arr = []
        for i in range(self.p.n):
            result = avg_waiting_time_in_system_arr[i] - (1 / self.p.mu)
            avg_waiting_time_in_queue_arr.append(result)

        return avg_waiting_time_in_queue_arr
    
    def avg_clients_in_system(self):
        avg_wait_in_system_arr = self.avg_waiting_time_in_system()
        avg_clients_in_system_arr = []

        for i in range(self.p.n):
            if i == 0:
                result = self.avg_clients_in_queue()[i] + (self.p.lmbds[i] / self.p.mu)
                avg_clients_in_system_arr.append(result)
                continue

            result = sum(self.p.lmbds[:i+1]) * avg_wait_in_system_arr[i]
            avg_clients_in_system_arr.append(result)

        return avg_clients_in_system_arr
    
    def avg_clients_in_queue(self):
        avg_clients_in_system_arr = self.avg_clients_in_system()
        avg_clients_in_queue_arr = []
        for i in range(self.p.n):
            if i == 0:
                nominator = (self.calculate_p0() * (self.p.total_lambda / self.p.mu)**self.p.s * self.p.rho)
                denominator = factorial(self.p.s) * (1 - self.p.rho)**2
                avg_clients_in_queue_arr.append(nominator / denominator)
                continue

            result = avg_clients_in_system_arr[i] - (sum(self.p.lmbds[:i+1]) / self.p.mu)
            avg_clients_in_queue_arr.append(result)

        return avg_clients_in_queue_arr
    
    def calculate_average_waiting_time_in_system(self, i):
        nominator = (self.calculate_p0() * ((sum(self.p.lmbds[:i+1]) / self.p.mu)**self.p.s) * self.p.rho)
        denominator = factorial(self.p.s) * (1 - self.p.rho)**2
        term1 = nominator / denominator
    
        return term1 + (sum(self.p.lmbds[:i+1]) / self.p.mu)

    def calculate_p0(self):
        summation = sum(((self.p.total_lambda / self.p.mu)**n) / factorial(n) for n in range(self.p.s))
        term1 = ((self.p.total_lambda / self.p.mu)**self.p.s) / factorial(self.p.s)
        term2 = 1 / (1 - (self.p.total_lambda / (self.p.s * self.p.mu)))
        return 1 / (summation + term1 * term2)