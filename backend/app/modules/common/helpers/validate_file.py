import os
from fastapi import UploadFile, File
from app.libraries.http.exception_library import ExceptionLibrary
from app.config.translations.i18n import get_translation
from app.libraries.file_library import FileLibrary
from app.config.settings import settings
from app.adapters.log_adapter import LogAdapter

async def validate_file(file: UploadFile = File(...), locale: str = settings.DEFAULT_LANGUAGE, allowed_extensions: set[str] = {'.xlsx', '.xls'}, allowed_mime_types: set[str] = {'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel'}, max_size_mb: int = 10):
    # 1. Validate file size
    file_size = await FileLibrary.get_file_size(file)
    ExceptionLibrary.throw_400_if(
        file_size > max_size_mb * 1024 * 1024,
        get_translation("errors.file_too_large", locale=locale, file=file.filename, max_size_mb=max_size_mb)
    )
    
    # 2. Validate file extension
    extension = os.path.splitext(file.filename or '')[1].lower()
    ExceptionLibrary.throw_400_if(
        not extension or extension not in allowed_extensions, 
        get_translation("errors.invalid_file", locale=locale, file=file.filename),
    )
    
    # 3. Validate file mime type
    mime_type = await FileLibrary.get_mime_type(file)
    ExceptionLibrary.throw_400_if(
        mime_type not in allowed_mime_types, 
        get_translation("errors.invalid_file", locale=locale, file=file.filename),
    )

    await file.seek(0)
    return file