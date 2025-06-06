from queues.mmsk.methods import method_options
from queues.mmsk.queue import MM1KQueue, MMSKQueue
from queues.mmsk.input import get_queue_data
from utils.utils import create_queue_window


def run():
    print("Bem-vindo ao simulador de filas M/M/s!")
    params = get_queue_data()

    queue = None
    if params.s == 1:
        queue = MM1KQueue(params)
    else:
        queue = MMSKQueue(params)

    create_queue_window(queue, method_options(queue))