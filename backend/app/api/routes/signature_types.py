import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    Message,
    SignatureType,
    SignatureTypeCreate,
    SignatureTypePublic,
    SignatureTypesPublic,
    SignatureTypeUpdate,
)

router = APIRouter(prefix="/signature-types", tags=["signature-types"])


@router.get("/", response_model=SignatureTypesPublic)
def read_signature_types(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> SignatureTypesPublic:
    """
    Retrieve signature types.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(SignatureType)
        count = session.exec(count_statement).one()
        statement = (
            select(SignatureType)
            .order_by(col(SignatureType.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        signature_types = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(SignatureType)
            .where(SignatureType.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(SignatureType)
            .where(SignatureType.owner_id == current_user.id)
            .order_by(col(SignatureType.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        signature_types = session.exec(statement).all()

    signature_types_public = [
        SignatureTypePublic.model_validate(signature_type)
        for signature_type in signature_types
    ]
    return SignatureTypesPublic(data=signature_types_public, count=count)


@router.get("/{id}", response_model=SignatureTypePublic)
def read_signature_type(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> SignatureType:
    """
    Get signature type by ID.
    """
    signature_type = session.get(SignatureType, id)
    if not signature_type:
        raise HTTPException(status_code=404, detail="Signature Type not found")
    if not current_user.is_superuser and (signature_type.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return signature_type


@router.post("/", response_model=SignatureTypePublic)
def create_signature_type(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    signature_type_in: SignatureTypeCreate,
) -> SignatureType:
    """
    Create new signature type.
    """
    signature_type = SignatureType.model_validate(
        signature_type_in, update={"owner_id": current_user.id}
    )
    session.add(signature_type)
    session.commit()
    session.refresh(signature_type)
    return signature_type


@router.put("/{id}", response_model=SignatureTypePublic)
def update_signature_type(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    signature_type_in: SignatureTypeUpdate,
) -> SignatureType:
    """
    Update an signature type.
    """
    signature_type = session.get(SignatureType, id)
    if not signature_type:
        raise HTTPException(status_code=404, detail="Signature Type not found")
    if not current_user.is_superuser and (signature_type.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = signature_type_in.model_dump(exclude_unset=True)
    _ = signature_type.sqlmodel_update(update_dict | {"updated_at": datetime.now(ZoneInfo("Europe/Moscow"))})
    session.add(signature_type)
    session.commit()
    session.refresh(signature_type)
    return signature_type


@router.delete("/{id}")
def delete_signature_type(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an signature type.
    """
    signature_type = session.get(SignatureType, id)
    if not signature_type:
        raise HTTPException(status_code=404, detail="Signature Type not found")
    if not current_user.is_superuser and (signature_type.owner_id != current_user.id):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(signature_type)
    session.commit()
    return Message(message="Signature Type deleted successfully")
