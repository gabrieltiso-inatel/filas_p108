from queues.priority_model.with_interruption.input import Params

class PriorityModelWithInterruptionQueue:
    def __init__(self, p: Params):
        self.lmbds = p.lmbds
        self.mu = p.mu
        self.s = p.s
        self.K = p.K
        self.p = p
        
    def avg_waiting_time_in_queue(self):
        lmbds_array = [self.lmbds]
        soma_k_1 = sum(lmbds_array[:self.K-1])
        soma_k = sum(lmbds_array[:self.K])
        den = 1 - (soma_k_1 + soma_k) / (self.s * self.mu)
        if den == 0:
            raise ZeroDivisionError("O denominador é zero, a expressão é indefinida.")
        W = (1 / self.mu) / den
        return W