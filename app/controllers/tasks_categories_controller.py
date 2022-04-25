from app.models.categories_model import Category
from app.models.tasks_model import Task
from app.models.tasks_categories_table import tasks_categories

from app.configs.database import db

def retrieve_all():
    query = db.session.query(Category, Task).select_from(Category).join(tasks_categories).join(Task).all()
    print(query)

    return ''