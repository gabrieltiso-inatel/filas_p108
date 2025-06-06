from queues.mg1.input import get_queue_data
from queues.mg1.queue import MG1Queue
from queues.mg1.methods import method_options
from utils.utils import create_queue_window

def run():
    params = get_queue_data()
    queue = MG1Queue(params)

    create_queue_window(queue, method_options(queue))