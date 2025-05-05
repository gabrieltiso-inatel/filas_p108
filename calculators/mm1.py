from measures import MeasuresCalculator
from queue_input_data import QueueInputData
import math

class MM1Calculator(MeasuresCalculator):
    def __init__(self, data: QueueInputData):
        self.lambda_param = data.lambda_param
        self.mi_param = data.mi_param
        super().__init__(data)

    def probability_system_busy(self) -> float:
        rho = self.lambda_param / self.mi_param
        return rho

    def probability_n_clients_in_system(self, n: int) -> float:
        rho = self.probability_system_busy()
        Pn = rho * (1 - rho) ** (n)
        return Pn
    
    def probability_n_clients_more_than_r(self, r: int) -> float:
        lambda_divided_by_mi = self.lambda_param / self.mi_param
        Pnr = lambda_divided_by_mi ** (r + 1)
        return Pnr
    
    def probability_system_idle(self) -> float:
        Pidle = 1 - self.probability_system_busy()
        return Pidle
    
    def probability_time_spent_in_system(self, t: float) -> float:
        rho = self.probability_system_busy()
        aux = (1 - rho)*t
        minus_mi = -1 * self.mi_param
        exp = aux * minus_mi
        Pwt = math.e ** exp
        return Pwt

    def probability_time_spent_in_queue(self, t: float) -> float:
        rho = self.probability_system_busy()
        probability_time_spent_in_system = self.probability_time_spent_in_system(t)
        PWqt = rho * probability_time_spent_in_system
        return PWqt

    def avg_time_spent_in_queue(self) -> float:
        Wq = self.lambda_param / (self.mi_param * (self.mi_param - self.lambda_param))
        return Wq
    
    def avg_number_of_clients_in_queue(self) -> float:
        Lq = self.avg_time_spent_in_queue() * self.lambda_param
        return Lq

    def avg_time_spent_in_system_per_client(self) -> float:
        W = 1 / (self.mi_param - self.lambda_param)
        return W

    def avg_number_of_clients_in_system(self) -> float:
        L = self.lambda_param * self.avg_time_spent_in_system_per_client()
        return L
