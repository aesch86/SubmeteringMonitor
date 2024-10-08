import time
from typing import Callable
from pydantic import BaseModel


class Task(BaseModel):
    name: str
    func: Callable
    interval: int
    next_run: float = None
    canceled: bool = False
    isRunning: bool = False
    isError: bool = False
    type: str = ""

    def __init__(self, **data):
        # super().__init__(**data)
        self.next_run = data.get('next_run', time.time())

    class Config:
        validate_assignment = True