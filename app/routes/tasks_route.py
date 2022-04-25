from flask import Blueprint
from app.controllers import tasks_controller

bp = Blueprint("tasks", __name__, url_prefix="/tasks")

bp.post("")(tasks_controller.create_task)
bp.patch("")(tasks_controller.update_task)
bp.delete("")(tasks_controller.delete_task)
#bp.errorhandler(404)(tasks_controller.error_not_found)
#bp.errorhandler(400)(tasks_controller.error_bad_request)