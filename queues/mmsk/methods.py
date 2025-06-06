from queues.mmsk.queue import MMSK, MM1KQueue
from tkinter import simpledialog

def method_options(queue: MMSK):
    if isinstance(queue, MM1KQueue):
        return {
            0: (
                "Probabilidade de n clientes no sistema (Pn)",
                lambda: queue.prob_n_clients_in_system(
                    simpledialog.askinteger("Parâmetro", "Digite o valor de n:")
                ),
            ),
            1: (
                "Probabilidade de o sistema estar vazio (P0)",
                queue.prob_zero_clients_in_system,
            ),
            2: (
                "Número médio de clientes no sistema (L)",
                queue.avg_number_clients_in_system,
            ),
            3: (
                "Número médio de clientes na fila (Lq)",
                queue.avg_number_clients_in_queue,
            ),
            4: (
                "Tempo médio no sistema (W)",
                queue.avg_wait_time_in_system,
            ),
            5: (
                "Tempo médio na fila (Wq)",
                queue.avg_wait_time_in_queue,
            ),
        }

    return {
        0: (
            "Probabilidade de n clientes no sistema (Pn)",
            lambda: queue.prob_n_clients_in_system(
                simpledialog.askinteger("Parâmetro", "Digite o valor de n:")
            ),
        ),
        1: (
            "Probabilidade de o sistema estar vazio (P0)",
            queue.prob_zero_clients_in_system,
        ),
        2: (
            "Número médio de clientes no sistema (L)",
            queue.avg_number_clients_in_system,
        ),
        3: (
            "Número médio de clientes na fila (Lq)",
            queue.avg_number_clients_in_queue,
        ),
        4: (
            "Tempo médio no sistema (W)",
            queue.avg_wait_time_in_system,
        ),
        5: (
            "Tempo médio na fila (Wq)",
            queue.avg_wait_time_in_queue,
        ),
    }