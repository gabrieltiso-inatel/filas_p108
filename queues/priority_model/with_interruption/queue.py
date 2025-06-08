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
        self.wait_in_system_arr = []

    def avg_waiting_time_in_system(self):
        return [self.w(i) for i in range(self.p.n)]
    
    def avg_waiting_time_in_queue(self):
        return [self.wq(i) for i in range(self.p.n)]
    
    def avg_clients_in_system(self):
        return [self.l(i) for i in range(self.p.n)]
    
    def avg_clients_in_queue(self):
        return [self.lq(i) for i in range(self.p.n)]

    def w(self, i):
        if i == 0:
            res = self.l(i) / self.p.lmbds[0]
            self.wait_in_system_arr.append(res)
            return res

        avg_w = self.wait_in_system_mms(i)
        percentages = [self.p.lmbds[j] / self.cummulative_lmbd(i) for j in range(i+1)]
        percentage_sum = sum([self.wait_in_system_arr[j] * percentages[j] for j in range(i)])

        res = (avg_w - percentage_sum) / percentages[i]
        self.wait_in_system_arr.append(res)
        return res


    def wq(self, i):
        return self.w(i) - (1 / self.p.mu)

    def l(self, i):
        if i == 0:
            return self.lq(i) + (self.p.lmbds[0] / self.p.mu)
        return self.cummulative_lmbd(i) * self.w(i)
    
    def lq(self, i):
        if i == 0:
            return self.wait_in_queue_mms(self.p.lmbds[0], self.cummulative_rho(self.p.lmbds[0]))
        return self.avg_clients_in_system()[i] - (self.cummulative_lmbd(i) / self.p.mu)

    def cummulative_rho(self, lmbd):
        return lmbd / (self.p.s * self.p.mu)

    def cummulative_lmbd(self, i):
        return sum(self.p.lmbds[:i+1])

    def wait_in_queue_mms(self, lmbd, rho):
        nominator = (self.p0(lmbd) * (lmbd / self.p.mu)**self.p.s * rho)
        denominator = factorial(self.p.s) * (1 - rho)**2
        return nominator / denominator
    
    def wait_in_system_mms(self, i):
        lmbd = self.cummulative_lmbd(i)
        lq = self.wait_in_queue_mms(lmbd, self.cummulative_rho(lmbd))

        return (lq + (lmbd / self.p.mu)) / lmbd

    def p0(self, lmbd):
        summation = sum(((lmbd / self.p.mu)**n) / factorial(n) for n in range(self.p.s))
        term1 = ((lmbd / self.p.mu)**self.p.s) / factorial(self.p.s)
        term2 = 1 / (1 - (lmbd / (self.p.s * self.p.mu)))

        return 1 / (summation + term1 * term2)
