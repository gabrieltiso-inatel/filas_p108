from utils.utils import queue_loop
from queues.priority_model.with_interruption.input import get_queue_data
from queues.priority_model.with_interruption.methods import method_options
from queues.priority_model.with_interruption.queue import PriorityModelWithInterruptionQueueOneServer

def run():
    print("Bem-vindo ao simulador de filas de prioridade com interrupção!")
    params = get_queue_data()
    queue = PriorityModelWithInterruptionQueueOneServer(params)

    queue_loop(queue, method_options(queue))