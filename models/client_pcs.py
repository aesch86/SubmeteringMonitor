from pydantic import BaseModel


class ClientPC(BaseModel):
    name:str
    url:str