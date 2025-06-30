from app.modules.users.models.user_model import User
from app.modules.auth.dependencies import protected_route
from fastapi import Depends
from app.libraries.http.exception_library import ExceptionLibrary

def view_all_roles(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.view"))
    return user

def view_role(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.view"))
    return user

def create_role(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.manage"))
    return user

def update_role(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.manage"))
    return user

def delete_role(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.delete"))
    return user

def delete_many_roles(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.delete"))
    return user

def export_roles(user: User = Depends(protected_route)):
    ExceptionLibrary.throw_403_if(not user.can("roles.can.manage"))
    return user
