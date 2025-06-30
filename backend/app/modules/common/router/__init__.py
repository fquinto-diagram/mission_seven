from fastapi import APIRouter
from app.modules.auth.routes.auth_routes import router as auth_router
from app.modules.roles.routes.roles_routes import router as roles_router
from app.modules.countries.routes.countries_routes import router as countries_router
from app.modules.companies.routes.company_routes import router as companies_router

router = APIRouter()

# Import and register the routers of the modules
# Example:
# from app.modules.routes import users_router
# router.include_router(users_router)

# Register the routers of the modules
router.include_router(auth_router)
router.include_router(companies_router)
router.include_router(countries_router)
router.include_router(roles_router)