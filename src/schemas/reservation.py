from datetime import datetime

from pydantic import BaseModel


class RequestReservation(BaseModel):
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_time: float

class ResponseReservation(BaseModel):
    id: int
    customer_name: str
    table_id: int
    reservation_time: datetime
    duration_time: float