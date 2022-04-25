from app.configs.database import db

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from dataclasses import dataclass

@dataclass
class Eisenhower(db.Model):
    id: int
    type: str

    __tablename__ = "eisenhowers"

    id = Column(Integer, primary_key=True)
    type = Column(String(100))

    #eisenhower = relationship("Task", back_populates="tasks")
