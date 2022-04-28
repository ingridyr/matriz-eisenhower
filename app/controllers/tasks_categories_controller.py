from flask import jsonify
from app.models.categories_model import Category
from app.models.tasks_model import Task
from app.models.eisenhowers_model import Eisenhower
from app.models.tasks_categories_table import tasks_categories

from app.configs.database import db

def retrieve_all():
    query = db.session.query(Category).all()
    list_categories = []

    for index in range(len(query)):

        category = {
            "id": query[index].id,
            "name": query[index].name,
            "description": query[index].description,
            "tasks": []
        }

        for item in query[index].tasks:
            task = {
                "id": item.id,
                "name": item.name,
                "description": item.description,
                "classification": (Eisenhower.query.get(item.eisenhower_id).type)
            }
            category["tasks"].append(task)

        list_categories.append(category)

    return jsonify(list_categories)