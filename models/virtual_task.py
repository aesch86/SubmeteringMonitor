# from Client.Scheduler.Models.Task import Task
import time
from enum import Enum
from typing import List, Callable
from pydantic import BaseModel, Field

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

class VirtualRegister(Enum):
    Spannung = 1
    Strom = 2
    Leistung = 3

class VirtualRegister(BaseModel):
    name: str
    amplitude: int
    noise_level: int
    duration: int
    offset: int


class VirtualTask(Task):
    type:str = "Virtual"
    virtual_register: List[VirtualRegister] = Field(default=[0])

    def __init__(self, **data):
        # super().__init__(**data)
        self.__dict__.update(data)
