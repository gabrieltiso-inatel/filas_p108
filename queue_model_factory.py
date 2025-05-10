from calculators.mm1 import MM1Calculator
from queue_input_data import QueueInputData

class QueueMeasureCalculatorFactory:
    def create(self, data: QueueInputData):
        if data.A == "M" and data.B == "M" and data.m == 1:
            return MM1Calculator(data)
        else:
            raise NotImplementedError("Modelo de fila ainda não implementado.")
