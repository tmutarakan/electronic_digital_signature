import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    CertificationCenter,
    CertificationCenterCreate,
    CertificationCenterPublic,
    CertificationCentersPublic,
    CertificationCenterUpdate,
)

router = APIRouter(prefix="/certification-centers", tags=["certification-centers"])


@router.get("/", response_model=CertificationCentersPublic)
def read_certification_centers(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> CertificationCentersPublic:
    """
    Retrieve Certification Centers.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(CertificationCenter)
        count = session.exec(count_statement).one()
        statement = (
            select(CertificationCenter)
            .order_by(col(CertificationCenter.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        certification_centers = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(CertificationCenter)
            .where(CertificationCenter.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(CertificationCenter)
            .where(CertificationCenter.owner_id == current_user.id)
            .order_by(col(CertificationCenter.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        certification_centers = session.exec(statement).all()

    certification_centers_public = [
        CertificationCenterPublic.model_validate(certification_center)
        for certification_center in certification_centers
    ]
    return CertificationCentersPublic(data=certification_centers_public, count=count)


@router.get("/{id}", response_model=CertificationCenterPublic)
def read_certification_center(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> CertificationCenter:
    """
    Get certification center by ID.
    """
    certification_center = session.get(CertificationCenter, id)
    if not certification_center:
        raise HTTPException(status_code=404, detail="Certification Center not found")
    if not current_user.is_superuser and (certification_center.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return certification_center


@router.post("/", response_model=CertificationCenterPublic)
def create_certification_center(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    certification_center_in: CertificationCenterCreate,
) -> CertificationCenter:
    """
    Create new certification center.
    """
    certification_center = CertificationCenter.model_validate(
        certification_center_in, update={"owner_id": current_user.id}
    )
    session.add(certification_center)
    session.commit()
    session.refresh(certification_center)
    return certification_center


@router.put("/{id}", response_model=CertificationCenterPublic)
def update_certification_center(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    certification_center_in: CertificationCenterUpdate,
) -> CertificationCenter:
    """
    Update an certification center.
    """
    certification_center = session.get(CertificationCenter, id)
    if not certification_center:
        raise HTTPException(status_code=404, detail="Certification Center not found")
    if not current_user.is_superuser and (certification_center.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = certification_center_in.model_dump(exclude_unset=True)
    _ = certification_center.sqlmodel_update(update_dict | {"updated_at": datetime.now(ZoneInfo("Europe/Moscow"))})
    session.add(certification_center)
    session.commit()
    session.refresh(certification_center)
    return certification_center


@router.delete("/{id}")
def delete_certification_center(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an certification center.
    """
    certification_center = session.get(CertificationCenter, id)
    if not certification_center:
        raise HTTPException(status_code=404, detail="Certification Center not found")
    if not current_user.is_superuser and (certification_center.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(certification_center)
    session.commit()
    return Message(message="Certification Center deleted successfully")
