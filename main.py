from input import InputCollector
from queue_model_factory import QueueMeasureCalculatorFactory


def main():
    collector = InputCollector()
    data = collector.collect()

    factory = QueueMeasureCalculatorFactory()
    calculator = factory.create(data)

    # TODO: Criar função que mostre os dados calculados.
    # Idealmente, deve ser mais uma interface que pede os
    # dados ao usuário e calcula os valores desejados 
    # usando as funções já definidas no calculator
    # específico

if __name__ == "__main__":
    main()
