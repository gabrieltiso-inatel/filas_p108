from queues.priority_model.with_interruption.queue import PriorityModelWithInterruptionQueueOneServer

from queues.priority_model.with_interruption.queue import (
    PriorityModelWithInterruptionQueueOneServer,
    PriorityModelWithInterruptionQueueWithParamsMultipleServers,
)

def method_options(queue):
    if isinstance(queue, PriorityModelWithInterruptionQueueOneServer):
        return {
            0: (
                "Tempo médio de espera no sistema",
                queue.avg_waiting_time_in_system
            ),
            1: (
                "Tempo médio de espera na fila",
                queue.avg_waiting_time_in_queue
            ),
            2: (
                "Número médio de clientes no sistema",
                queue.avg_clients_in_system
            ),
            3: (
                "Número médio de clientes na fila",
                queue.avg_clients_in_queue
            )
        }

    return {
        0: (
            "Tempo médio de espera no sistema",
            queue.avg_waiting_time_in_system
        ),
        1: (
            "Tempo médio de espera na fila",
            queue.avg_waiting_time_in_queue
        ),
        2: (
            "Número médio de clientes no sistema",
            queue.avg_clients_in_system
        ),
        3: (
            "Número médio de clientes na fila",
            queue.avg_clients_in_queue
        )
    }