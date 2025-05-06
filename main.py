from input import InputCollector
from output import run_menu
from queue_model_factory import QueueMeasureCalculatorFactory


def main():
    collector = InputCollector()
    data = collector.collect()

    factory = QueueMeasureCalculatorFactory()
    calculator = factory.create(data)

    run_menu(calculator)

if __name__ == "__main__":
    main()
