from app.configs.database import db
from sqlalchemy import Column, Integer, ForeignKey
from dataclasses import dataclass

@dataclass
class Task_category(db.Model):
    id: int
    task_id: int
    category_id: int

    __tablename__ = "tasks_categories"

    id = Column(Integer, primary_key=True)

    task_id = Column(Integer, ForeignKey("tasks.id"), nullable=False)
    category_id = Column(Integer, ForeignKey("categories.id"), nullable=False)