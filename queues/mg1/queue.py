from queues.mg1.input import Params

class MG1Queue:
    def __init__(self, p: Params):
        self.p = p

    def prob_zero_clients_in_system(self):
        return 1 - self.p.rho
    
    def avg_num_clients_in_queue(self):
        return (self.p.lmbd**2 * self.p.deviation + self.p.rho**2) / (2*(1 - self.p.rho))
    
    def avg_waiting_time_in_queue(self):
        return self.avg_num_clients_in_queue() / self.p.lmbd
    
    def avg_num_clients_in_system(self):
        return self.avg_num_clients_in_queue() + self.p.rho
    
    def avg_waiting_time_in_system(self):
        return self.avg_waiting_time_in_queue() + (1 / self.p.mu)
    