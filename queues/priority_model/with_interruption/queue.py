from queues.priority_model.with_interruption.input import Params

class PriorityModelWithInterruptionQueue:
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