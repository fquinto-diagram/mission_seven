import json
from app.config.worker import celery
from app.modules.companies.repositories.company_repository import CompanyRepository
from app.config.worker import redis_client
from app.config.database import SessionLocal
from app.adapters.log_adapter import LogAdapter
from fastapi.encoders import jsonable_encoder

@celery.task(name="app.modules.companies.tasks.delete_many_companies_task")
def delete_many_companies_task(job_id: str, company_ids: list[int], completed: int, total: int):
    db = SessionLocal()
    try:
        company_repository = CompanyRepository(db)
        company_repository.delete_many(company_ids)
        message = json.dumps(jsonable_encoder({
            "ok": True if completed >= total else False,
            "job_id": 'delete_many_companies_task',
            "progress": f"{completed}/{total}",
            "total": total,
            "completed": min(completed, total),
            "percentage": min(round(completed / total * 100, 0), 100),
        }))
        redis_client.publish(str(job_id), message)
    except Exception as e:
        LogAdapter.error(f"Error deleting companies in task {job_id}: {str(e)}")
        raise e
    finally:
        db.close()
celery.tasks.register(delete_many_companies_task)
