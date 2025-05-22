from queues.mg1.input import get_queue_data
from queues.mg1.queue import MG1Queue
from queues.mg1.methods import method_options
from utils.utils import queue_loop

def run():
    print("Bem-vindo ao simulador de filas MG1!")

    params = get_queue_data()
    queue = MG1Queue(params)

    queue_loop(queue, method_options(queue))