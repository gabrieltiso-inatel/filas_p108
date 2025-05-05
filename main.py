from input import InputCollector
from queue_model_factory import QueueMeasureCalculatorFactory
from calculators import mm1
from outputs import mm1 as mm1_output


def main():
    collector = InputCollector()
    data = collector.collect()

    factory = QueueMeasureCalculatorFactory()
    calculator = factory.create(data)
    
    if isinstance(calculator, mm1.MM1Calculator):
        mm1_output.show_menu(calculator)
        
if __name__ == "__main__":
    main()
