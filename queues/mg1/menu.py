from queues.mg1.input import get_queue_data
from queues.mg1.queue import MG1Queue
from queues.mg1.methods import method_options
from utils.utils import create_queue_window

def run():
    print("Bem-vindo ao simulador de filas M/G/1!")

    params = get_queue_data()
    queue = MG1Queue(params)

    create_queue_window(queue, method_options(queue))