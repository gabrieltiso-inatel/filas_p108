from queues.mms.input import get_queue_data
from queues.mms.queue import MMsQueue, MM1Queue
from queues.mms.methods import method_options

from utils.utils import create_queue_window

def run():
    print("Bem-vindo ao simulador de filas M/M/s!")
    params = get_queue_data()

    queue = None
    if params.s == 1:
        queue = MM1Queue(params)
    else:
        queue = MMsQueue(params)

    create_queue_window(queue, method_options(queue))