from http import HTTPStatus
from flask import jsonify, request

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session

from app.configs.database import db
from app.models.categories_model import Category


def create_category():
    session: Session = db.session()

    data = request.get_json()

    category = Category(**data)

    session.add(category)

    try:
        session.commit()

        return jsonify(category), HTTPStatus.CREATED
        
    except IntegrityError:
        return {"error": "Category already exists"}, HTTPStatus.CONFLICT


def update_category(id):
    session: Session = db.session()
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
    session: Session = db.session()

    category = session.query(Category).get(id)

    if category == None:
        return {"error": "Category id not found"}, HTTPStatus.NOT_FOUND

    session.delete(category)
    session.commit()

    return "", HTTPStatus.NO_CONTENT