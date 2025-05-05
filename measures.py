from abc import ABC, abstractmethod

from queue_input_data import QueueInputData

class MeasuresCalculator(ABC):
    def __init__(self, data: QueueInputData):
        self.data = data;

    @abstractmethod
    def probability_n_clients_in_system(self, n: int) -> float:
        pass
