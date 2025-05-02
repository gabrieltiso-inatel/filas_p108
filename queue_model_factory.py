from calculators.mm1 import MM1Calculator
from calculators.mms import MMSCalculator
from measures import MeasuresCalculator
from queue_input_data import QueueInputData

class QueueMeasureCalculatorFactory:
    # TODO: dar sequência e definir as outras filas
    def create(self, data: QueueInputData) -> MeasuresCalculator:
        calculator_map = {
            ('M', 'M', 1): MM1Calculator,
            ('M', 'M', 'multi'): MMSCalculator
        }
        
        key = (data.A, data.B, 1 if data.m == 1 else 'multi')
        calculator_class = calculator_map.get(key)
        
        if calculator_class:
            return calculator_class(data)
        raise NotImplementedError("Modelo de fila ainda não implementado.")
