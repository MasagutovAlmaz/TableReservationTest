from decimal import Decimal

from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, Float, Numeric
from sqlalchemy.orm import relationship

from src.db import Base
class Reservation(Base):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    table_id = Column(Integer, ForeignKey("table.id"))
    reservation_time = Column(DateTime(timezone=True))
    duration_time = Column(Numeric(10, 2), index=True)

    table = relationship("Table", back_populates="reservations")