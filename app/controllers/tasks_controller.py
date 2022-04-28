from flask import jsonify, request
from http import HTTPStatus

from app.models import Eisenhower
from app.models import Task
from app.models.categories_model import Category

from app.configs.database import db

from psycopg2.errors import UniqueViolation

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

def get_eisenhower(importance, urgency):

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

    return eisenhower_type_id


def create_task():
    session: Session = db.session()

    data = request.get_json()

    importance = data["importance"]
    urgency = data["urgency"]
    data['name'] = data['name'].title()

    if importance > 2 or importance < 1:
        return {"error": "Importance should be 1 or 2"}, HTTPStatus.BAD_REQUEST
    
    if urgency > 2 or urgency < 1:
        return {"error": "Urgency should be 1 or 2"}, HTTPStatus.BAD_REQUEST

    eisenhower_type_id = get_eisenhower(data["importance"], data["urgency"])
    data['eisenhower_id'] = eisenhower_type_id

    valid_keys = ["id", "name", "description", "duration", "importance", "urgency", "eisenhower_id"]
    new_data = {key: value for key, value in data.items() if key in valid_keys}

    task = Task(**new_data)

    try:
        for item in data['categories']:
            category = Category.query.filter(Category.name == item.title()).first()

            if category == None and item != None:
                category: Category = Category(
                    name=item.title(),
                    description='No content'
                    )

                category.tasks.append(task)
                session.add(category)
                session.commit()

            if category:
                category.tasks.append(task)
                session.add(category)
                session.commit()
        
        classification = Eisenhower.query.filter_by(id=eisenhower_type_id).first().type
        
        session.add(task)
        session.commit()
            
        return jsonify({
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "duration": task.duration,
                "classification": classification,
                "category": [item.title() for item in data['categories']]
            }), HTTPStatus.OK

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"error": "Task already exists"}, HTTPStatus.CONFLICT


def update_task(id):
    session: Session = db.session()

    try:
        data = request.get_json()
        task: Task = Task.query.get(id)
        
        if "importance" in data.keys() and "urgency" in data.keys():
            if data["importance"] > 2 or data["importance"] < 1:
                return {"error": "Importance should be 1 or 2"}, HTTPStatus.BAD_REQUEST
    
            if data["urgency"] > 2 or data["urgency"] < 1:
                return {"error": "Urgency should be 1 or 2"}, HTTPStatus.BAD_REQUEST
            
            eisenhower_type_id = get_eisenhower(data["importance"], data["urgency"])
            data['eisenhower_id'] = eisenhower_type_id
 
        elif "urgency" in data.keys():
            if data["urgency"] > 2 or data["urgency"] < 1:
                return {"error": "Urgency should be 1 or 2"}, HTTPStatus.BAD_REQUEST
            
            eisenhower_type_id = get_eisenhower(task.importance, data["urgency"])
            data['eisenhower_id'] = eisenhower_type_id

        elif "importance" in data.keys():
            if data["importance"] > 2 or data["importance"] < 1:
                return {"error": "Importance should be 1 or 2"}, HTTPStatus.BAD_REQUEST
 
            eisenhower_type_id = get_eisenhower(data["importance"], task.urgency)
            data['eisenhower_id'] = eisenhower_type_id
        
        if "name" in data.keys():
            data["name"] = data["name"].title()

        if task == None:
            return {"error": "Task id not found"}, HTTPStatus.NOT_FOUND

        for key, value in data.items():
            setattr(task, key, value)

        session.add(task)
        session.commit()

        return {
                "id": task.id,
                "name": task.name,
                "description": task.description,
                "duration": task.duration,
                "eisenhower": (Eisenhower.query.get(task.eisenhower_id).type)
            }

    except KeyError:
        return {"error": "key error"}, HTTPStatus.BAD_REQUEST

    except IntegrityError as e:
        if type(e.orig) == UniqueViolation:
            return {"error": "Task already exists"}, HTTPStatus.CONFLICT

def delete_task(id):
    session: Session = db.session()
    task: Task = Task.query.get(id)

    if task == None:
        return {"error": "Task not found"}, HTTPStatus.NOT_FOUND

    session.delete(task)
    session.commit()

    return "", HTTPStatus.NO_CONTENT