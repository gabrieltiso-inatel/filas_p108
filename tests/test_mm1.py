import pytest
from calculators.mm1 import MM1Calculator
from queue_input_data import QueueInputData

@pytest.mark.parametrize(
    "lambda_param, mi_param, expected",
    [
        (0.3, 0.4, 0.25),
        (0.2, 0.1, 0),
        (0.5, 0.2, 0),
    ]
)
def test_probability_zero_clients_in_system(lambda_param, mi_param, expected):
    input_data = QueueInputData("M", "M", 1, "FCFS", K=None, N=None,
                                 lambda_param=lambda_param, mi_param=mi_param)
    calculator = MM1Calculator(input_data)
    assert calculator.probability_zero_clients_in_system() == pytest.approx(expected)