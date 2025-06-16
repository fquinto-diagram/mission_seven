from datetime import datetime
from app.config.worker import celery
from app.adapters.log_adapter import LogAdapter
from app.adapters.excel_adapter import ExcelAdapter
import os
from app.config.database import SessionLocal
from app.modules.roles.repositories.role_repository import RoleRepository
from app.modules.common.helpers.storage_path import storage_path
from app.adapters.mail_adapter import MailAdapter
from app.modules.users.repositories.user_repository import UserRepository
from app.config.translations.i18n import get_translation
import asyncio
from app.libraries.file_library import FileLibrary

@celery.task(name="app.modules.roles.tasks.export_roles_task")
def export_roles_task(user_id: int, role_ids: list[int] = None, from_date: str = None, to_date: str = None):
    storage_dir = storage_path("roles", str(user_id))
    
    storage_dir.mkdir(parents=True, exist_ok=True)
    if from_date:
        file_name = f"export_roles_{datetime.strptime(from_date, '%Y-%m-%d').strftime('%Y-%m-%d')}_{datetime.strptime(to_date, '%Y-%m-%d').strftime('%Y-%m-%d')}.xlsx"
    else:
        file_name = f"export_roles_{datetime.now().strftime('%Y-%m-%d')}.xlsx"
    excel_path = os.path.join(storage_dir, file_name)
    
    db = SessionLocal()
    role_repository = RoleRepository(db)
    user_repository = UserRepository(db)
    user = user_repository.find(user_id)
    if from_date:
        ExcelAdapter().export_by_date_range(file_name=str(excel_path), headers=['name'], retrieve_callback=lambda x: role_repository.scope_date_range(role_repository._base_query(), from_date, to_date, limit=100, page=x), locale=user.lang)
    else:
        ExcelAdapter().export_with_chunks(file_name=str(excel_path), items=role_ids, headers=['name'], retrieve_callback=lambda x: role_repository.find_many(x), locale=user.lang)
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
