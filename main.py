from input import InputCollector
from output import run_menu
from queue_model_factory import QueueMeasureCalculatorFactory
from calculators import mm1
import output


def main():
    collector = InputCollector()
    data = collector.collect()

    factory = QueueMeasureCalculatorFactory()
    calculator = factory.create(data)
    
    if isinstance(calculator, mm1.MM1Calculator):
        output.run_menu(calculator)
        
if __name__ == "__main__":
    main()
