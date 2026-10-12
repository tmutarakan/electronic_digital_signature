import uuid

from fastapi import APIRouter

from app import crud
from app.api.deps import CurrentUser, SessionDep, SuperUser
from app.models import (
    CertificationCenter,
    CertificationCenterCreate,
    CertificationCenterPublic,
    CertificationCentersPublic,
    CertificationCenterUpdate,
    Message,
)

router = APIRouter(prefix="/certification-centers", tags=["certification-centers"])


@router.get("/", response_model=CertificationCentersPublic)
def read_certification_centers(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> CertificationCentersPublic:
    """
    Retrieve Certification Centers. Доступно всем аутентифицированным пользователям.
    """
    items, count = crud.list_all(session, CertificationCenter, skip, limit)
    return CertificationCentersPublic(
        data=[CertificationCenterPublic.model_validate(x) for x in items],
        count=count,
    )


@router.get("/{id}", response_model=CertificationCenterPublic)
def read_certification_center(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> CertificationCenter:
    """
    Get certification center by ID. Доступно всем аутентифицированным пользователям.
    """
    return crud.get_or_404(session, CertificationCenter, id)


@router.post("/", response_model=CertificationCenterPublic)
def create_certification_center(
    *,
    session: SessionDep,
    current_user: SuperUser,
    certification_center_in: CertificationCenterCreate,
) -> CertificationCenter:
    """
    Create new certification center. Только для суперпользователя.
    """
    return crud.create_certification_center(
        session=session,
        certification_center_in=certification_center_in,
        owner_id=current_user.id,
    )


@router.put("/{id}", response_model=CertificationCenterPublic)
def update_certification_center(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    certification_center_in: CertificationCenterUpdate,
) -> CertificationCenter:
    """
    Update a certification center. Только для суперпользователя.
    """
    obj = crud.get_or_404(session, CertificationCenter, id)
    return crud.update_obj(session, obj, certification_center_in)


@router.delete("/{id}")
def delete_certification_center(
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
) -> Message:
    """
    Delete a certification center. Только для суперпользователя.
    """
    obj = crud.get_or_404(session, CertificationCenter, id)
    session.delete(obj)
    session.commit()
    return Message(message="Certification Center deleted successfully")
