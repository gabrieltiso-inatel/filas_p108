from queues.mg1.queue import MG1Queue

def method_options(queue: MG1Queue):
    return {
        0: (
            "Probabilidade de o sistema estar vazio (P0)",
            queue.prob_zero_clients_in_system
        ),
        1: (
            "Número médio de clientes na fila (Lq)",
            queue.avg_num_clients_in_queue
        ),
        2: (
            "Tempo médio de espera na fila (Wq)",
            queue.avg_waiting_time_in_queue
        ),
        3: (
            "Número médio de clientes no sistema (L)",
            queue.avg_num_clients_in_system
        ),
        4: (
            "Tempo médio de espera no sistema (W)",
            queue.avg_waiting_time_in_system
        )
    } 