import uuid

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
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
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> OrganizationsPublic:
    """
    Retrieve organizations.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(Organization)
        count = session.exec(count_statement).one()
        statement = (
            select(Organization)
            .order_by(col(Organization.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        organizations = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(Organization)
            .where(Organization.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(Organization)
            .where(Organization.owner_id == current_user.id)
            .order_by(col(Organization.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        organizations = session.exec(statement).all()

    organizations_public = [
        OrganizationPublic.model_validate(organization)
        for organization in organizations
    ]
    return OrganizationsPublic(data=organizations_public, count=count)


@router.get("/{id}", response_model=OrganizationPublic)
def read_organization(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Organization:
    """
    Get organization by ID.
    """
    organization = session.get(Organization, id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not current_user.is_superuser and (organization.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return organization


@router.post("/", response_model=OrganizationPublic)
def create_organization(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    organization_in: OrganizationCreate,
) -> Organization:
    """
    Create new organization.
    """
    organization = Organization.model_validate(
        organization_in, update={"owner_id": current_user.id}
    )
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization


@router.put("/{id}", response_model=OrganizationPublic)
def update_organization(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    organization_in: OrganizationUpdate,
) -> Organization:
    """
    Update an organization.
    """
    organization = session.get(Organization, id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not current_user.is_superuser and (organization.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = organization_in.model_dump(exclude_unset=True)
    _ = organization.sqlmodel_update(update_dict)
    session.add(organization)
    session.commit()
    session.refresh(organization)
    return organization


@router.delete("/{id}")
def delete_organization(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an organization.
    """
    organization = session.get(Organization, id)
    if not organization:
        raise HTTPException(status_code=404, detail="Organization not found")
    if not current_user.is_superuser and (organization.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(organization)
    session.commit()
    return Message(message="Organization deleted successfully")
