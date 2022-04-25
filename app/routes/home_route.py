from flask import Blueprint
from app.controllers import home_controller

bp = Blueprint("home", __name__, url_prefix="/")

bp.get("")(home_controller.get_all)