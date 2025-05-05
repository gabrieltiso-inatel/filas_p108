from dataclasses import dataclass
from typing import Optional

@dataclass
class QueueInputData:
    A: str
    B: str
    m: int
    C: str
    K: Optional[int]
    N: Optional[int]
    lambda_param: float
    mi_param: float