import time
from typing import Callable, Dict, List
from pydantic import BaseModel, Field
from models.task import Task


class Values(BaseModel):
    limits_ok: Dict[str, bool] = Field(default=None)
    last_values: Dict[str, float] = Field(default=None)

class AnomalyTask(Task):
    task_name: str = Field(default="")
    critcal_limits: Dict[str, float] = Field(default=dict)
    values: Values = Field(default_factory=None)
    characteristics: List[str] = Field(default_factory=list)
    registers_to_be_checked: List[str] = Field(default_factory=list)
    def __init__(self, **data):
        # super().__init__(**data)
        # self.next_run = data.get('next_run', time.time())
        self.__dict__.update(data)
    class Config:
        validate_assignment = True
