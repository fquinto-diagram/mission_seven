from app.modules.users.models.user_model import User
from app.modules.auth.dependencies import protected_route
from fastapi import Depends
from app.libraries.http.exception_library import ExceptionLibrary

def view_all_companies(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.view"))
    return user

def view_company(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.view"))
    return user

def create_company(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.manage"))
    return user

def update_company(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.manage"))
    return user

def delete_company(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.delete"))
    return user

def delete_many_companies(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.delete"))
    return user

def export_companies(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.manage"))
    return user

def import_companies(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("companies.can.manage"))
    return user