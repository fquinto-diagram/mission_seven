from app.config.worker import celery
from .delete_many_roles_task import delete_many_roles_task
from .export_roles_task import export_roles_task

__all__ = ["delete_many_roles_task", "export_roles_task"]

celery.tasks.register(delete_many_roles_task)
celery.tasks.register(export_roles_task)