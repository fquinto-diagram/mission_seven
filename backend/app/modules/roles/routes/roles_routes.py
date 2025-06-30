from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from app.modules.roles.dependencies import get_role_repository
from app.modules.roles.repositories.role_repository import RoleRepository
from fastapi.encoders import jsonable_encoder
from app.modules.users.models.user_model import User
from app.modules.roles.policies.role_policy import view_all_roles, view_role, create_role, update_role, delete_role, delete_many_roles, export_roles
from app.modules.roles.schemas import RoleFilter, RoleCreate, RoleUpdate, RoleResponseSchema, RolesResponseSchema, PermissionResponseSchema, RoleCreateResponseSchema, RoleUpdateResponseSchema, RoleDeleteResponseSchema, RoleDeleteMany, RoleExportSchema
from app.config.translations.i18n import get_translation
from app.modules.roles.dependencies import get_permissions_repository
from app.modules.roles.repositories.permissions_repository import PermissionsRepository
from app.modules.common.helpers.send_task_with_chunks import send_task_with_chunks
from app.adapters.worker_adapter import WorkerAdapter
from app.config.settings import settings
from app.adapters.excel_adapter import ExcelAdapter

router = APIRouter(prefix="/roles", tags=["roles"])

@router.get("", response_model=RolesResponseSchema)
async def get_roles(query: RoleFilter = Depends(), user: User = Depends(view_all_roles), role_repository: RoleRepository = Depends(get_role_repository)):
    roles = role_repository.list(query)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder(roles)
    )

@router.post("", response_model=RoleCreateResponseSchema)
async def store_role(request: RoleCreate, user: User = Depends(create_role), role_repository: RoleRepository = Depends(get_role_repository)):
    role = role_repository.create(request)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({
            "message": get_translation("roles.created", locale=user.lang), 
            "role": role 
        })
    )

@router.get("/permissions", response_model=PermissionResponseSchema)
async def get_permissions(user: User = Depends(view_all_roles), permissions_repository: PermissionsRepository = Depends(get_permissions_repository)):
    permissions = permissions_repository.all()
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({ "data": permissions })
    )
    
@router.delete("/delete-many", response_model=RoleDeleteResponseSchema)
async def delete_many_roles(request: RoleDeleteMany, user: User = Depends(delete_many_roles)):
    send_task_with_chunks(f"user-{user.id}", "app.modules.roles.tasks.delete_many_roles_task", request.ids)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({ "message": get_translation("common.data_processing", locale=user.lang) })
    )

@router.get("/{id}", response_model=RoleResponseSchema)
async def get_role(id: int, query: RoleFilter = Depends(), user: User = Depends(view_role), role_repository: RoleRepository = Depends(get_role_repository)):
    role = role_repository.find(id, query.include)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder({ "role": role })
    )

@router.put("/{id}", response_model=RoleUpdateResponseSchema)
async def update_role(id: int, request: RoleUpdate, user: User = Depends(update_role), role_repository: RoleRepository = Depends(get_role_repository)):
    role = role_repository.update(id, request)
    return JSONResponse(
        status_code=200, content=jsonable_encoder({
            "message": get_translation("roles.updated", locale=user.lang),
            "role": role 
        })
    )

@router.delete("/{id}", response_model=RoleDeleteResponseSchema)
async def delete_role(id: int, query: RoleFilter = Depends(), user: User = Depends(delete_role), role_repository: RoleRepository = Depends(get_role_repository)):
    role_repository.delete(id)
    roles = role_repository.list(query)
    roles["message"] = get_translation("roles.deleted", locale=user.lang)
    return JSONResponse(
        status_code=200, 
        content=jsonable_encoder(roles)
    )
    
@router.post("/export/excel")
async def export_roles_excel(request: RoleExportSchema, user: User = Depends(export_roles), role_repository: RoleRepository = Depends(get_role_repository)):
    if request.ids and len(request.ids) < settings.PROJECT_CHUNK_SIZE:
        roles = role_repository.find_many(request.ids)
        roles_data = role_repository.to_dict(roles)
        excel_data = ExcelAdapter().create_excel(roles_data, ['name'], locale=user.lang)
        return jsonable_encoder({
            "file": excel_data
        })
    worker_adapter = WorkerAdapter()
    worker_adapter.send("app.modules.roles.tasks.export_roles_task", kwargs={
        'user_id': user.id,
        "role_ids": request.ids,
        "from_date": request.from_date,
        "to_date": request.to_date
    })
    return jsonable_encoder({
        "message": get_translation("common.email_data_processing", locale=user.lang)
    })