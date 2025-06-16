from datetime import datetime
from app.config.worker import celery
from app.adapters.excel_adapter import ExcelAdapter
import os
from app.config.database import SessionLocal
from app.modules.companies.repositories.company_repository import CompanyRepository
from app.modules.common.helpers.storage_path import storage_path
from app.adapters.mail_adapter import MailAdapter
from app.modules.users.repositories.user_repository import UserRepository
from app.config.translations.i18n import get_translation
import asyncio
from app.config.settings import settings
from app.libraries.file_library import FileLibrary

@celery.task(name="app.modules.companies.tasks.export_companies_task")
def export_companies_task(user_id: int, company_ids: list[int] = None, from_date: str = None, to_date: str = None):
    storage_dir = storage_path("companies", str(user_id))
    
    storage_dir.mkdir(parents=True, exist_ok=True)
    if from_date:
        file_name = f"export_companies_{datetime.strptime(from_date, '%Y-%m-%d').strftime('%Y-%m-%d')}_{datetime.strptime(to_date, '%Y-%m-%d').strftime('%Y-%m-%d')}.xlsx"
    else:
        file_name = f"export_companies_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    excel_path = os.path.join(storage_dir, file_name)
    
    db = SessionLocal()
    company_repository = CompanyRepository(db)
    user_repository = UserRepository(db)
    user = user_repository.find(user_id)
    headers = ['legal_name', 'trade_name', 'cif', 'address', 'city', 'country', 'province', 'phone', 'email', 'web']
    if from_date:
        ExcelAdapter().export_by_date_range(file_name=str(excel_path), headers=headers, retrieve_callback=lambda page: company_repository.scope_date_range(company_repository._base_query(), from_date, to_date, limit=settings.PROJECT_CHUNK_SIZE, page=page), relationships={'country': 'name'}, locale=user.lang)
    else:
        ExcelAdapter().export_with_chunks(file_name=str(excel_path), items=company_ids, headers=headers, retrieve_callback=lambda x: company_repository.find_many(x, include_relations=['country']), relationships={'country': 'name'}, locale=user.lang)
    mail = MailAdapter(locale=user.lang)
    
    asyncio.run(mail.send_email(
        template=os.path.join("common", "export_mail.html"),
        to=user.email,
        body={
            "name": user.name,
        },
        subject=get_translation("common.export_mail_subject", user.lang),
        files=[{
            "file": str(excel_path),
            "filename": file_name,
            "mime_type": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        }]
    ))
    FileLibrary.delete_file(excel_path)
