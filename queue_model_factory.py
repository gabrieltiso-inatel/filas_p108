from calculators.mm1 import MM1Calculator
from calculators.mms import MMSCalculator
from measures import MeasuresCalculator
from queue_input_data import QueueInputData

class QueueMeasureCalculatorFactory:
    # TODO: dar sequência e definir as outras filas
    def create(self, data: QueueInputData) -> MeasuresCalculator:
        if data.A == "M" and data.B == "M" and data.m == 1:
            return MM1Calculator(data)
        elif data.A == "M" and data.B == "M" and data.m > 1:
            return MMSCalculator(data)
        raise NotImplementedError("Modelo de fila ainda não implementado.")
