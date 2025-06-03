from queues.priority_model.with_interruption.queue import PriorityModelWithInterruptionQueue

def method_options(queue: PriorityModelWithInterruptionQueue):
    if isinstance(queue, PriorityModelWithInterruptionQueue):
        return {
            0: (
                "Tempo médio de espera na fila",
                queue.avg_waiting_time_in_queue,
            )
        }
