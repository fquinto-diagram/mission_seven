import json
import os
from app.config.worker import celery
from app.config.worker import redis_client
from app.config.database import SessionLocal
from app.adapters.log_adapter import LogAdapter
from fastapi.encoders import jsonable_encoder
from app.modules.companies.repositories.company_repository import CompanyRepository
from app.modules.countries.repositories.country_repository import CountryRepository
from app.modules.users.repositories.user_repository import UserRepository
from app.modules.companies.schemas import CompanyCreateSchema
from app.libraries.file_library import FileLibrary
from app.adapters.mail_adapter import MailAdapter
from app.config.translations.i18n import get_translation
import asyncio
from app.modules.common.helpers.create_txt import create_txt
from app.modules.common.helpers.storage_path import storage_path

@celery.task(name="app.modules.companies.tasks.import_companies_task")
def import_companies_task(job_id: str, chunk: list, total: int, completed: int, file_path: str = None, user_id: int = None):
    db = SessionLocal()
    try:
        company_repository = CompanyRepository(db)
        country_repository = CountryRepository(db)
        errors = []
        user_repository = UserRepository(db)
        user = user_repository.find(user_id)
        for row in chunk:
            try:
                if 'country_id' in row:
                    country = country_repository.get_by_name(row['country_id'])
                    row['country_id'] = country.id if country else 56
                else:
                    row['country_id'] = 56
                if 'phone' in row:
                    row['phone'] = str(row['phone'])
                company = company_repository.find_by_unique_fields({
                    "legal_name": row['legal_name'],
                    "trade_name": row['trade_name'],
                    "cif": row['cif']
                })
                if not company:
                    company_repository.create(CompanyCreateSchema(**row))
            except Exception as e:
                errors.append(f"{get_translation('common.error_importing_data', locale=user.lang)}: {e}")
        
        is_completed = True if completed >= total else False
        message = json.dumps(jsonable_encoder({
            "ok": is_completed,
            "job_id": 'import_companies_task',
            "progress": f"{completed}/{total}",
            "total": total,
            "completed": min(completed, total),
            "percentage": min(round(completed / total * 100, 0), 100),
        }))
        redis_client.publish(str(job_id), message)
        if is_completed:
            FileLibrary.delete_file(file_path)
            if errors:
                mail = MailAdapter(locale=user.lang)

                errors_storage_path = storage_path("companies", str(user.id))
                file_name = 'errors.txt'
                errors_file = os.path.join(errors_storage_path, file_name)
                create_txt(errors_file, errors)
                asyncio.run(mail.send_email(
                    template=os.path.join("common", "errors_mail.html"),
                    to=user.email,
                    body={
                        "name": user.name,
                    },
                    subject=get_translation("common.errors_mail_subject", locale=user.lang),
                    files=[{
                        "file": str(errors_file),
                        "filename": file_name,
                        "mime_type": "text/plain"
                    }]
                ))
                FileLibrary.delete_file(errors_file)
                
    except Exception as e:
        LogAdapter.error(f"Error importing companies in task {job_id}: {str(e)}")
        raise e
    finally:
        db.close()
celery.tasks.register(import_companies_task)
