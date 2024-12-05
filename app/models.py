from pydantic import BaseModel

class Player(BaseModel):
    name: str
    money: int
    score: int