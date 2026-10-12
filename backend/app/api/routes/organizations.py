import uuid

from fastapi import APIRouter

from app import crud
from app.api.deps import CurrentUser, SessionDep, SuperUser
from app.models import (
    Message,
    Organization,
    OrganizationCreate,
    OrganizationPublic,
    OrganizationsPublic,
    OrganizationUpdate,
)

router = APIRouter(prefix="/organizations", tags=["organizations"])


@router.get("/", response_model=OrganizationsPublic)
def read_organizations(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> OrganizationsPublic:
    """
    Retrieve organizations. Доступно всем аутентифицированным пользователям.
    """
    items, count = crud.list_all(session, Organization, skip, limit)
    return OrganizationsPublic(
        data=[OrganizationPublic.model_validate(x) for x in items],
        count=count,
    )


@router.get("/{id}", response_model=OrganizationPublic)
def read_organization(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> Organization:
    """
    Get organization by ID. Доступно всем аутентифицированным пользователям.
    """
    return crud.get_or_404(session, Organization, id)


@router.post("/", response_model=OrganizationPublic)
def create_organization(
    *,
    session: SessionDep,
    current_user: SuperUser,
    organization_in: OrganizationCreate,
) -> Organization:
    """
    Create new organization. Только для суперпользователя.
    owner_id проставляется автоматически для аудита.
    """
    return crud.create_organization(
        session=session,
        organization_in=organization_in,
        owner_id=current_user.id,
    )


@router.put("/{id}", response_model=OrganizationPublic)
def update_organization(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    organization_in: OrganizationUpdate,
) -> Organization:
    """
    Update an organization. Только для суперпользователя.
    """
    organization = crud.get_or_404(session, Organization, id)
    return crud.update_obj(session, organization, organization_in)


@router.delete("/{id}")
def delete_organization(
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
) -> Message:
    """
    Delete an organization. Только для суперпользователя.
    """
    organization = crud.get_or_404(session, Organization, id)
    session.delete(organization)
    session.commit()
    return Message(message="Organization deleted successfully")
