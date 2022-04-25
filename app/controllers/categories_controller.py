from http import HTTPStatus
from sqlalchemy.exc import IntegrityError
from app.models.categories_model import Category

from flask import jsonify, request, current_app

def create_category():
    session = current_app.db.session

    data = request.get_json()

    category = Category(**data)

    session.add(category)

    try:
        session.commit()

        return jsonify(category), HTTPStatus.CREATED
        
    except IntegrityError:
        return {"error": "Category already exists"}, HTTPStatus.CONFLICT


def update_category(id):
    session = current_app.db.session
    data = request.get_json()

    category = session.query(Category).get(id)

    if category == None:
        return {"error": "Category id not found"}, HTTPStatus.NOT_FOUND

    for key, value in data.items():
        setattr(category, key, value)

    session.add(category)
    session.commit()

    return jsonify(category), HTTPStatus.OK


def delete_category(id):
    session = current_app.db.session

    category = session.query(Category).get(id)

    if category == None:
        return {"error": "Category id not found"}, HTTPStatus.NOT_FOUND

    session.delete(category)
    session.commit()

    return "", HTTPStatus.NO_CONTENT