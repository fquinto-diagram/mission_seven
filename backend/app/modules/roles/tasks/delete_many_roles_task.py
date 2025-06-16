import json
from app.config.worker import celery
from app.modules.roles.repositories.role_repository import RoleRepository
from app.config.worker import redis_client
from app.config.database import SessionLocal
from app.adapters.log_adapter import LogAdapter
from fastapi.encoders import jsonable_encoder

@celery.task(name="app.modules.roles.tasks.delete_many_roles_task")
def delete_many_roles_task(job_id: str, role_ids: list[int], completed: int, total: int):
    db = SessionLocal()
    try:
        role_repository = RoleRepository(db)
        role_repository.delete_many(role_ids)
        message = json.dumps(jsonable_encoder({
            "ok": True if completed >= total else False,
            "job_id": 'delete_many_roles_task',
            "progress": f"{completed}/{total}",
            "total": total,
            "completed": min(completed, total),
            "percentage": min(round(completed / total * 100, 0), 100),
        }))
        redis_client.publish(str(job_id), message)
    except Exception as e:
        LogAdapter.error(f"Error deleting roles in task {job_id}: {str(e)}")
        raise e
    finally:
        db.close()

