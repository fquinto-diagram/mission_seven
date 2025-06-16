from fastapi import APIRouter, Depends
from app.modules.companies.policies.company_policy import view_all_companies, view_company, create_company, update_company, delete_company, delete_many_companies, export_companies, import_companies
from app.modules.companies.repositories.company_repository import CompanyRepository
from app.modules.companies.schemas import CompanyFilterSchema, CompanyCreateSchema, CompanyUpdateSchema, CompaniesResponseSchema, CompanyCreateResponseSchema, CompanyUpdateResponseSchema, CompanyDeleteResponseSchema, CompanyDeleteMany, CompanyExportSchema, CompanyImportResponseSchema
from app.modules.companies.models.company_model import Company
from app.modules.users.models.user_model import User
from app.modules.companies.dependencies import get_company_repository
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from app.config.translations.i18n import get_translation
from app.modules.common.helpers.send_task_with_chunks import send_task_with_chunks
from app.config.settings import settings
from app.adapters.worker_adapter import WorkerAdapter
from app.modules.common.helpers.validate_file import validate_file
from fastapi import UploadFile, File
from app.libraries.file_library import FileLibrary
from app.adapters.excel_adapter import ExcelAdapter

router = APIRouter(
    prefix="/companies",
    tags=["companies"],
)

@router.get("", response_model=CompaniesResponseSchema)
async def get_companies(query: CompanyFilterSchema = Depends(), user: User = Depends(view_all_companies), company_repository: CompanyRepository = Depends(get_company_repository)):
    companies = company_repository.list(query, search_fields=Company.SEARCH_FIELDS, filters=query.filters)
    return JSONResponse(content=jsonable_encoder(companies))

@router.post("", response_model=CompanyCreateResponseSchema)
async def create_company(request: CompanyCreateSchema, user: User = Depends(create_company), company_repository: CompanyRepository = Depends(get_company_repository)):
    company = company_repository.create(request)
    return JSONResponse(content=jsonable_encoder({"message": get_translation("companies.created", locale=user.lang), "company": company}))

@router.get("/{id}")
async def get_company(id: int, query: CompanyFilterSchema = Depends(), user: User = Depends(view_company), company_repository: CompanyRepository = Depends(get_company_repository)):
    company = company_repository.find(id, query.include)
    return JSONResponse(content=jsonable_encoder({"company": company}))

@router.put("/{id}", response_model=CompanyUpdateResponseSchema)
async def update_company(id: int, request: CompanyUpdateSchema, user: User = Depends(update_company), company_repository: CompanyRepository = Depends(get_company_repository)):
    company = company_repository.update(id, request)
    return JSONResponse(content=jsonable_encoder({"message": get_translation("companies.updated", locale=user.lang), "company": company}))

@router.delete("/{id}", response_model=CompanyDeleteResponseSchema)
async def destroy_company(id: int, query: CompanyFilterSchema = Depends(), user: User = Depends(delete_company), company_repository: CompanyRepository = Depends(get_company_repository)):
    company_repository.delete(id)
    companies = company_repository.list(query, search_fields=Company.SEARCH_FIELDS)
    companies['message'] = get_translation("companies.deleted", locale=user.lang)
    return JSONResponse(content=jsonable_encoder(companies))

@router.delete("/delete/many", response_model=CompanyDeleteResponseSchema)
async def destroy_companies(request: CompanyDeleteMany, user: User = Depends(delete_many_companies)):
    send_task_with_chunks(f"user-{user.id}", "app.modules.companies.tasks.delete_many_companies_task", request.ids)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({ "message": get_translation("common.data_processing", locale=user.lang) })
    )
    
@router.post("/export/excel")
async def export_companies(request: CompanyExportSchema, user: User = Depends(export_companies), company_repository: CompanyRepository = Depends(get_company_repository)):
    if len(request.ids) > 0 and len(request.ids) < settings.PROJECT_CHUNK_SIZE:
        companies = company_repository.find_many(request.ids, include_relations=['country'])
        companies_data = company_repository.to_dict(companies, include_relations=['country'])
        excel_data = ExcelAdapter().create_excel(companies_data, ['legal_name', 'trade_name', 'cif', 'address', 'country', 'city', 'province', 'phone', 'email', 'web'], relationships={'country': 'name'}, locale=user.lang)
        return jsonable_encoder({
            "file": excel_data
        })
    worker_adapter = WorkerAdapter()
    worker_adapter.send("app.modules.companies.tasks.export_companies_task", kwargs={
        'user_id': user.id,
        "company_ids": request.ids,
        "from_date": request.from_date,
        "to_date": request.to_date
    })
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({ "message": get_translation("common.email_data_processing", locale=user.lang) })
    )
    
@router.post("/import/excel", response_model=CompanyImportResponseSchema)
async def import_companies(file: UploadFile = File(...), user: User = Depends(import_companies)):
    await validate_file(file, locale=user.lang)
    file_path = await FileLibrary.temp_file(file, user_id=user.id)
    excel_adapter = ExcelAdapter()
    total = excel_adapter.count_rows(file_path)
    worker_adapter = WorkerAdapter()
    for index, chunk in  enumerate(excel_adapter.read_excel_with_chunks(file_path)):
        completed = (index + 1) * settings.PROJECT_CHUNK_SIZE
        worker_adapter.send("app.modules.companies.tasks.import_companies_task", kwargs={ 
            "job_id": f"user-{user.id}",
            "chunk": chunk,
            "total": total,
            "completed":  completed,
            "file_path": file_path,
            "user_id": user.id
        })
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({ "message": get_translation("common.data_processing", locale=user.lang) })
    )   