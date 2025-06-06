from utils.utils import create_queue_window
from queues.priority_model.with_interruption.input import get_queue_data
from queues.priority_model.with_interruption.methods import method_options
from queues.priority_model.with_interruption.queue import PriorityModelWithInterruptionQueue

def run():
    print("Bem-vindo ao simulador de filas de prioridade com interrupção!")
    params = get_queue_data()
    queue = PriorityModelWithInterruptionQueue(params)

    create_queue_window(queue, method_options(queue))