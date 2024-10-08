import time
from pydantic import BaseModel, Field
from typing import List, Callable

from models.task import Task


class ModbusCredentials(BaseModel):
    NAME: str = Field(default="NSHV")
    HOST: str = Field(default="192.168.200.100")
    PORT: int = Field(default= 502)
    UNIT_ID: int = Field(default= 1)
    TIMEOUT: int = Field(default= 2)
    AUTO_OPEN: bool = Field(default= True)

    def __hash__(self):
        # Hier wird eine Tupel verwendet, um den Hashwert zu berechnen
        return hash((self.HOST, self.PORT, self.UNIT_ID, self.TIMEOUT, self.AUTO_OPEN))

    def to_dict(self):
        return {
            "HOST": self.HOST,
            "PORT": self.PORT,
            "UNIT_ID": self.UNIT_ID,
            "TIMEOUT": self.TIMEOUT,
            "AUTO_OPEN": self.AUTO_OPEN,
        }

    class Config:
        validate_assignment = True


default = ModbusCredentials

# class Task(BaseModel):
#     name: str
#     func: str
#     interval: int
#     next_run: float = None
#     canceled: bool = False
#     isRunning: bool = False
#     isError: bool = False
#     type: str = ""
#
#     def __init__(self, **data):
#         # super().__init__(**data)
#         self.next_run = data.get('next_run', time.time())
#
#     class Config:
#         validate_assignment = True

class ModbusAddr(BaseModel):
    name: str = Field(default="Register")
    addr: int = Field(default= True)
    type: str =  Field(default="float")
    nb: int = Field(default=1)

class ModbusTask(Task):

    def __init__(self, **data):
        # super().__init__(**data)
        self.__dict__.update(data)
        # type: str = "Modbus"
        # self.credentials: ModbusCredentials = data["credentials"]

    MODBUS_ADDR: List[ModbusAddr] = Field(default=[19000])
    type: str
    credentials: ModbusCredentials
    send_via: str = ""  # means which protocol
    send_interface: str = ""  # ethernet or 5G

    class Config:
        validate_assignment = True