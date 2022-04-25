from app.configs.database import db

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from dataclasses import dataclass

@dataclass
class Task(db.Model):
    id: int
    name: str
    description: str
    duration: int
    importance: int
    urgency: int
    eisenhower_id: int

    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String)
    duration = Column(Integer)
    importance = Column(Integer)
    urgency = Column(Integer)
    eisenhower_id = Column(Integer, ForeignKey("eisenhowers.id"), nullable=False)

    tasks_eisenhowers = relationship("Eisenhower", back_populates="eisenhowers")
    categories = relationship("Category", secondary="tasks_categories", back_populates="tasks")
