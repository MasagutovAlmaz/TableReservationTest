from pydantic import BaseModel


class RequestTable(BaseModel):
    name: str
    seats: int
    location: str

class ResponseTable(BaseModel):
    id: int
    name: str
    seats: int
    location: str