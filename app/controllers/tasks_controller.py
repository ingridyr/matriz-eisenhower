from flask import jsonify, request
from http import HTTPStatus

from app.models import Eisenhower
from app.models import Task
from app.models.categories_model import Category

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from app.configs.database import db

def create_task():
    session: Session = db.session()

    data = request.get_json()

    importance = data["importance"]
    urgency = data["urgency"]

    if importance > 2 or importance < 1:
        return {"error": "Importance should be 1 or 2"}, HTTPStatus.BAD_REQUEST
    
    if urgency > 2 or urgency < 1:
        return {"error": "Urgency should be 1 or 2"}, HTTPStatus.BAD_REQUEST

    if urgency == 1:
        if importance == 1:
            eisenhower_type_id = 1
        else:
            eisenhower_type_id = 2

    else:
        if importance == 1:
            eisenhower_type_id = 3
        else:
            eisenhower_type_id = 4

    data['eisenhower_id'] = eisenhower_type_id

    valid_keys = ["id", "name", "description", "duration", "importance", "urgency", "eisenhower_id"]

    new_data = {key: value for key, value in data.items() if key in valid_keys}

    task = Task(**new_data)

    for item in data['categories']:
        category = Category.query.filter(Category.name == item).first()

        if category == None and item != None:
            category: Category = Category(
                name=item,
                description='No content')
            
            category.tasks.append(task)
            session.add(category)
            session.commit()
        
        if category:
            category.tasks.append(task)
            session.add(category)
            session.commit()
            
    try:
        classification = Eisenhower.query.filter_by(id=eisenhower_type_id).first().type

        session.add(task)
        session.commit()

        return {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "duration": task.duration,
                "classification": classification,
                "category": data['categories']
            }

    except IntegrityError:
        return {"error": "Task already exists"}, HTTPStatus.CONFLICT

def update_task():
    ...

def delete_task(id):
    session: Session = db.session()
    task = Task.query.get(id)

    if not task:
        return {"error": "Task not found"}, HTTPStatus.NOT_FOUND

    session.delete(task)
    session.commit()

    return "", HTTPStatus.NO_CONTENT