from app.configs.database import db

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.models.tasks_categories_table import tasks_categories
from app.models.tasks_model import Task

from dataclasses import dataclass

@dataclass
class Category(db.Model):
    id: int
    name: str
    description: str
    tasks: Task

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String)


    tasks = relationship("Task", secondary=tasks_categories, back_populates="categories")
