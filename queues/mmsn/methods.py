from queues.mmsn.queue import MMNQueue, MM1NQueue, MMsNQueue

def method_options(queue: MMNQueue):
    if isinstance(queue, MM1NQueue):
        return {
            0: (
                "Probabilidade de n clientes no sistema (Pn)",
                lambda: queue.prob_n_clients_in_system(
                    int(input("Digite o valor de n: "))
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
                queue.avg_time_in_system,
            ),
            5: (
                "Tempo médio na fila (Wq)",
                queue.avg_waiting_time_in_queue,
            ),
        }

    elif isinstance(queue, MMsNQueue):
        return {
            0: (
                "Probabilidade de n clientes no sistema (Pn)",
                lambda: queue.prob_n_clients_in_system(
                    int(input("Digite o valor de n: "))
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
                queue.avg_time_in_system,
            ),
            5: (
                "Tempo médio na fila (Wq)",
                queue.avg_time_in_queue,
            ),
        }
