from fastapi import Request
import contextvars
from app.libraries.http.exception_library import ExceptionLibrary

company_id_ctx_var = contextvars.ContextVar("company_id")

def get_company_id(request: Request):
    company_id = request.headers.get("X-Company-Id")
    ExceptionLibrary.throw_401_if(not company_id or not company_id.isdigit(), "errors.missing_company_id_header")
    token = company_id_ctx_var.set(int(company_id))
    try:
        yield
    finally:
        company_id_ctx_var.reset(token)

def get_global_company_id():
    try:
        return company_id_ctx_var.get()
    except LookupError:
        return None
