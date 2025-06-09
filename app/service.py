from typing import Dict, Any, List
import sys, os

# Add the parent directory to the path to find the queues module
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from queues.mg1.queue import MG1Queue
from queues.mg1.input import Params as MG1Params

from queues.mms.queue import MM1Queue, MMsQueue
from queues.mms.input import Params as MMSParams

from queues.mmsn.queue import MM1NQueue, MMsNQueue
from queues.mmsn.input import Params as MMSNParams

from queues.mmsk.queue import MM1KQueue, MMSKQueue
from queues.mmsk.input import Params as MMSKParams

from queues.priority_model.with_interruption.queue import (
    PriorityModelWithInterruptionQueueOneServer,
    PriorityModelWithInterruptionQueueWithParamsMultipleServers
)
from queues.priority_model.with_interruption.input import Params as PriorityParams

class StreamlitQueueService:
    
    def calculate_mg1(self, lmbd: float, avg_service_time: float, service_time_variance: float) -> Dict[str, Any]:
        """Calculate M/G/1 queue metrics"""
        if lmbd <= 0 or avg_service_time <= 0 or service_time_variance <= 0:
            raise ValueError("All parameters must be positive")
        
        params = MG1Params(lmbd, avg_service_time, service_time_variance)
        queue = MG1Queue(params)
        
        return {
            "prob_zero_clients": queue.prob_zero_clients_in_system(),
            "avg_clients_in_queue": queue.avg_num_clients_in_queue(),
            "avg_wait_time_in_queue": queue.avg_waiting_time_in_queue(),
            "avg_clients_in_system": queue.avg_num_clients_in_system(),
            "avg_wait_time_in_system": queue.avg_waiting_time_in_system()
        }

    def calculate_mms(self, lmbd: float, mu: float, s: int) -> Dict[str, Any]:
        """Calculate M/M/s queue metrics"""
        if lmbd <= 0 or mu <= 0 or s < 1:
            raise ValueError("Lambda and mu must be positive, s must be at least 1")
        
        params = MMSParams(lmbd, mu, s)
        
        if s == 1:
            queue = MM1Queue(params)
            return {
                "prob_zero_clients": queue.prob_system_empty(),
                "avg_clients_in_system": queue.avg_number_clients_in_system(),
                "avg_clients_in_queue": queue.avg_number_clients_in_queue(),
                "avg_wait_time_in_system": queue.avg_time_in_system_per_client(),
                "avg_wait_time_in_queue": queue.avg_time_in_queue_per_client(),
                "prob_system_busy": queue.prob_system_busy()
            }
        else:
            queue = MMsQueue(params)
            return {
                "prob_zero_clients": queue.prob_zero_clients_in_system(),
                "avg_clients_in_system": queue.avg_number_clients_in_system(),
                "avg_clients_in_queue": queue.avg_number_clients_in_queue(),
                "avg_wait_time_in_system": queue.avg_time_in_system(),
                "avg_wait_time_in_queue": queue.avg_time_in_queue(),
                "prob_system_busy": 1 - queue.prob_zero_clients_in_system()
            }

    def calculate_mms_prob_n(self, lmbd: float, mu: float, s: int, n: int) -> float:
        """Get probability of n clients in M/M/s system"""
        params = MMSParams(lmbd, mu, s)
        
        if s == 1:
            queue = MM1Queue(params)
            return queue.prob_n_clients_in_system(n)
        else:
            queue = MMsQueue(params)
            return queue.prob_n_clients_in_system(n)

    def calculate_mms_prob_wait(self, lmbd: float, mu: float, s: int, t: float, wait_type: str) -> float:
        """Get probability of wait time > t in M/M/s system"""
        params = MMSParams(lmbd, mu, s)
        
        if s == 1:
            queue = MM1Queue(params)
            if wait_type == "system":
                return queue.prob_wait_in_system_bigger_than(t)
            else:
                return queue.prob_wait_in_queue_bigger_than(t)
        else:
            queue = MMsQueue(params)
            if wait_type == "system":
                return queue.prob_time_spent_in_system_bigger_than(t)
            else:
                return queue.prob_time_spent_in_queue_bigger_than(t)

    def calculate_mmsn(self, lmbd: float, mu: float, s: int, n: int) -> Dict[str, Any]:
        """Calculate M/M/s/n queue metrics"""
        if lmbd <= 0 or mu <= 0 or s < 1 or n < 1:
            raise ValueError("All parameters must be positive")
        
        params = MMSNParams(lmbd, mu, s, n)
        
        if s == 1:
            queue = MM1NQueue(params)
            return {
                "prob_zero_clients": queue.prob_zero_clients_in_system(),
                "avg_clients_in_system": queue.avg_number_clients_in_system(),
                "avg_clients_in_queue": queue.avg_number_clients_in_queue(),
                "avg_wait_time_in_system": queue.avg_time_in_system(),
                "avg_wait_time_in_queue": queue.avg_waiting_time_in_queue()
            }
        else:
            queue = MMsNQueue(params)
            return {
                "prob_zero_clients": queue.prob_zero_clients_in_system(),
                "avg_clients_in_system": queue.avg_number_clients_in_system(),
                "avg_clients_in_queue": queue.avg_number_clients_in_queue(),
                "avg_wait_time_in_system": queue.avg_time_in_system(),
                "avg_wait_time_in_queue": queue.avg_time_in_queue()
            }

    def calculate_mmsn_prob_n(self, lmbd: float, mu: float, s: int, n: int, target_n: int) -> float:
        """Get probability of target_n clients in M/M/s/n system"""
        params = MMSNParams(lmbd, mu, s, n)
        
        if s == 1:
            queue = MM1NQueue(params)
        else:
            queue = MMsNQueue(params)
            
        return queue.prob_n_clients_in_system(target_n)

    def calculate_mmsk(self, lmbd: float, mu: float, s: int, K: int) -> Dict[str, Any]:
        """Calculate M/M/s/K queue metrics"""
        if lmbd <= 0 or mu <= 0 or s < 1 or K < 1:
            raise ValueError("All parameters must be positive")
        
        params = MMSKParams(lmbd, mu, s, K)
        
        if s == 1:
            queue = MM1KQueue(params)
            return {
                "prob_zero_clients": queue.prob_zero_clients_in_system(),
                "avg_clients_in_system": queue.avg_number_clients_in_system(),
                "avg_clients_in_queue": queue.avg_number_clients_in_queue(),
                "avg_wait_time_in_system": queue.avg_wait_time_in_system(),
                "avg_wait_time_in_queue": queue.avg_wait_time_in_queue(),
                "avg_effective_arrival_rate": queue.avg_effective_arrival_rate()
            }
        else:
            queue = MMSKQueue(params)
            return {
                "prob_zero_clients": queue.prob_zero_clients_in_system(),
                "avg_clients_in_system": queue.avg_number_clients_in_system(),
                "avg_clients_in_queue": queue.avg_number_clients_in_queue(),
                "avg_wait_time_in_system": queue.avg_wait_time_in_system(),
                "avg_wait_time_in_queue": queue.avg_wait_time_in_queue(),
                "avg_effective_arrival_rate": queue.avg_effective_arrival_rate()
            }

    def calculate_mmsk_prob_n(self, lmbd: float, mu: float, s: int, K: int, target_n: int) -> float:
        """Get probability of target_n clients in M/M/s/K system"""
        params = MMSKParams(lmbd, mu, s, K)
        
        if s == 1:
            queue = MM1KQueue(params)
        else:
            queue = MMSKQueue(params)
            
        return queue.prob_n_clients_in_system(target_n)

    def calculate_priority_single_server(self, n: int, lmbds: List[float], mu: float, s: int, total_lambda: float) -> Dict[str, Any]:
        """Calculate priority queue with single server"""
        if len(lmbds) != n:
            raise ValueError(f"Number of lambdas ({len(lmbds)}) must match n ({n})")
        
        if not all(x > 0 for x in lmbds) or mu <= 0:
            raise ValueError("All rates must be positive")
        
        params = PriorityParams(n, lmbds, mu, s, total_lambda)
        queue = PriorityModelWithInterruptionQueueOneServer(params)
        
        return {
            "avg_waiting_time_in_system": queue.avg_waiting_time_in_system(),
            "avg_waiting_time_in_queue": queue.avg_waiting_time_in_queue(),
            "avg_clients_in_system": queue.avg_clients_in_system(),
            "avg_clients_in_queue": queue.avg_clients_in_queue()
        }

    def calculate_priority_multiple_servers(self, n: int, lmbds: List[float], mu: float, s: int, total_lambda: float) -> Dict[str, Any]:
        """Calculate priority queue with multiple servers"""
        if len(lmbds) != n:
            raise ValueError(f"Number of lambdas ({len(lmbds)}) must match n ({n})")
        
        if not all(x > 0 for x in lmbds) or mu <= 0:
            raise ValueError("All rates must be positive")
        
        params = PriorityParams(n, lmbds, mu, s, total_lambda)
        queue = PriorityModelWithInterruptionQueueWithParamsMultipleServers(params)
        
        return {
            "avg_waiting_time_in_system": queue.avg_waiting_time_in_system(),
            "avg_waiting_time_in_queue": queue.avg_waiting_time_in_queue(),
            "avg_clients_in_system": queue.avg_clients_in_system(),
            "avg_clients_in_queue": queue.avg_clients_in_queue()
        }