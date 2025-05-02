from abc import ABC, abstractmethod

from queue_input_data import QueueInputData

class MeasuresCalculator(ABC):
    def __init__(self, data: QueueInputData):
        self.data = data;

    ### PROBABILISTIC (CLIENTS IN THE MODEL) ##
    @abstractmethod
    def probability_zero_clients_in_system(self) -> float:
        pass

    @abstractmethod
    def probability_n_clients_in_system(self, n: int) -> float:
        pass

    ### PROBABILISTIC WAITING TIMES (WITH THRESHOLD) ##
    @abstractmethod
    def probability_time_spent_in_queue(self, t: int) -> float:
        pass

    @abstractmethod
    def probability_time_spent_in_system(self, t: int) -> float:
        pass

    ### AVERAGE (NUMBER) ##
    @abstractmethod
    def avg_number_of_clients_in_queue(self) -> float:
        pass

    @abstractmethod
    def avg_number_of_clients_in_system(self) -> float:
        pass

    ### AVERAGE (TIME) ##
    @abstractmethod
    def time_spent_in_queue(self) -> float:
        pass

    @abstractmethod
    def time_spent_in_system(self) -> float:
        pass
