from fastapi import APIRouter

from app.api.routes import (
    certification_centers,
    electronic_digital_signatures,
    employees,
    items,
    login,
    organizations,
    private,
    signature_types,
    users,
    utils,
)
from app.core.config import settings

api_router = APIRouter()
api_router.include_router(login.router)
api_router.include_router(users.router)
api_router.include_router(utils.router)
api_router.include_router(items.router)
api_router.include_router(organizations.router)
api_router.include_router(certification_centers.router)
api_router.include_router(electronic_digital_signatures.router)
api_router.include_router(employees.router)
api_router.include_router(signature_types.router)


if settings.FASTAPI_ENV == "development":
    api_router.include_router(private.router)
