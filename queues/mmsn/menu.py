from queues.mmsn.input import get_queue_data
from queues.mmsn.queue import MM1NQueue, MMsNQueue
from queues.mmsn.methods import method_options

from utils.utils import queue_loop

def run():
    print("Bem-vindo ao simulador de filas M/M/s/n")
    params = get_queue_data()

    queue = None
    if params.s == 1:
        queue = MM1NQueue(params)
    else:
        queue = MMsNQueue(params)

    queue_loop(queue, method_options(queue))