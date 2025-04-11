from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base


class Table(Base):
    __tablename__ = "table"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    seats = Column(Integer, index=True)
    location = Column(String, index=True)

    reservations = relationship("Reservation", back_populates="table")