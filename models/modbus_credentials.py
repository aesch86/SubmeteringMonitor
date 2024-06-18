from pydantic import BaseModel, Field

class ModbusCredentials(BaseModel):
    HOST: str = Field(default="192.168.200.100")
    PORT: int = Field(default= 502)
    UNIT_ID: int = Field(default= 1)
    TIMEOUT: int = Field(default= 2)
    AUTO_OPEN: bool = Field(default= True)


    class Config:
        validate_assignment = True

    def __hash__(self):
        # Hier wird eine Tupel verwendet, um den Hashwert zu berechnen
        return hash((self.HOST, self.PORT, self.UNIT_ID, self.TIMEOUT, self.AUTO_OPEN, self.NB))

    def to_dict(self):
        return {
            "HOST": self.HOST,
            "PORT": self.PORT,
            "UNIT_ID": self.UNIT_ID,
            "TIMEOUT": self.TIMEOUT,
            "AUTO_OPEN": self.AUTO_OPEN,
            "NB": self.NB
        }
