from queues.mms.queue import MMQueue, MM1Queue

def method_options(queue: MMQueue):
    if isinstance(queue, MM1Queue):
        return {
            0: (
                "Probabilidade de n clientes no sistema (Pn)",
                lambda: queue.prob_n_clients_in_system(
                    int(input("Digite o valor de n: "))
                ),
            ),
            1: (
                "Probabilidade de o sistema estar vazio (P0)",
                queue.prob_system_empty,
            ),
            2: (
                "Probabilidade de o sistema estar ocupado (1 - P0)",
                queue.prob_system_busy,
            ),
            3: (
                "Número médio de clientes no sistema (L)",
                queue.avg_number_clients_in_system,
            ),
            4: (
                "Número médio de clientes na fila (Lq)",
                queue.avg_number_clients_in_queue,
            ),
            5: (
                "Tempo médio no sistema (W)",
                queue.avg_time_in_system_per_client,
            ),
            6: (
                "Tempo médio na fila (Wq)",
                queue.avg_time_in_queue_per_client,
            ),
            7: (
                "Probabilidade de tempo de espera no sistema maior que t (P(W > t))",
                lambda: queue.prob_wait_in_system_bigger_than(
                    float(input("Digite o valor de t: "))
                ),
            ),
            8: (
                "Probabilidade de tempo de espera na fila maior que t (P(Wq > t))",
                lambda: queue.prob_wait_in_queue_bigger_than(
                    float(input("Digite o valor de t: "))
                ),
            ),
        }

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
        6: (
            "Probabilidade de tempo de espera no sistema maior que t (P(W > t))",
            lambda: queue.prob_time_spent_in_system_bigger_than(
                float(input("Digite o valor de t: "))
            ),
        ),
        7: (
            "Probabilidade de tempo de espera na fila maior que t (P(Wq > t))",
            lambda: queue.prob_time_spent_in_queue_bigger_than(
                float(input("Digite o valor de t: "))
            ),
        ),
    }