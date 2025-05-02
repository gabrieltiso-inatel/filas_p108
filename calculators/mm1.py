from measures import MeasuresCalculator
from queue_input_data import QueueInputData

class MM1Calculator(MeasuresCalculator):
    def __init__(self, data: QueueInputData):
        super().__init__(data)

    def probability_zero_clients_in_system(self) -> float:
        return 0

    def probability_n_clients_in_system(self, n: int) -> float:
        return 0

    def probability_time_spent_in_queue(self, t: int) -> float:
        return 0

    def probability_time_spent_in_system(self, t: int) -> float:
        return 0

    def avg_number_of_clients_in_queue(self) -> float:
        return 0

    def avg_number_of_clients_in_system(self) -> float:
        return 0

    def time_spent_in_queue(self) -> float:
        return 0

    def time_spent_in_system(self) -> float:
        return 0
