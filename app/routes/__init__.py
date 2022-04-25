from flask import Flask

from .categories_route import bp as bp_categories
from .tasks_route import bp as bp_tasks
from .tasks_categories_route import bp as bp_tasks_categories

def init_app(app: Flask):

    app.register_blueprint(bp_tasks_categories)
    app.register_blueprint(bp_categories)
    app.register_blueprint(bp_tasks)