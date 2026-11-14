from fastapi import APIRouter
from sqlmodel import func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    DashboardStats,
    ElectronicDigitalSignature,
    Employee,
    Organization,
)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])


def _count(session: SessionDep, model) -> int:
    """COUNT с учётом прав: суперпользователь — всё, остальные — только своё."""
    stmt = select(func.count()).select_from(model)
    return session.exec(stmt).one()


@router.get("/stats", response_model=DashboardStats)
def read_dashboard_stats(
    session: SessionDep,
    _current_user: CurrentUser,
) -> DashboardStats:
    """Счётчики организаций, сотрудников и подписей для дашборда."""
    return DashboardStats(
        organizations=_count(session, Organization),
        employees=_count(session, Employee),
        signatures=_count(session, ElectronicDigitalSignature),
    )
