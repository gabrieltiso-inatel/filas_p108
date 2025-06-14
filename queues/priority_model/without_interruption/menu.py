from utils.utils import queue_loop
from queues.priority_model.without_interruption.input import get_queue_data
from queues.priority_model.without_interruption.methods import method_options
from queues.priority_model.without_interruption.queue import PriorityModelWithoutInterruption

def run():
    print("Bem-vindo ao simulador de filas de prioridade sem interrupção!")
    params = get_queue_data()
    queue = PriorityModelWithoutInterruption(params)
    queue_loop(queue, method_options(queue))