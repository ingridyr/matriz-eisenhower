from app.configs.database import db
from sqlalchemy import Column, Integer, String, DateTime
from dataclasses import dataclass

@dataclass
class Category(db.Model):
    id: int
    name: str
    email: str
    phone: str
    creation_date: str
    last_visit: str
    visits: int

    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False, unique=True)
    description = Column(String)