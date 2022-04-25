from flask import Blueprint
from app.controllers import categories_controller

bp = Blueprint("categories", __name__, url_prefix="/categories")

bp.post("")(categories_controller.create_category)
bp.patch("")(categories_controller.update_category)
bp.delete("")(categories_controller.delete_category)
#bp.errorhandler(404)(categories_controller.error_not_found)
#bp.errorhandler(400)(categories_controller.error_bad_request)