import uuid

from fastapi import APIRouter

from app import crud
from app.api.deps import CurrentUser, SessionDep, SuperUser
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
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> SignatureTypesPublic:
    items, count = crud.list_all(session, SignatureType, skip, limit)
    return SignatureTypesPublic(
        data=[SignatureTypePublic.model_validate(x) for x in items],
        count=count,
    )


@router.get("/{id}", response_model=SignatureTypePublic)
def read_signature_type(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> SignatureType:
    return crud.get_or_404(session, SignatureType, id)


@router.post("/", response_model=SignatureTypePublic)
def create_signature_type(
    *,
    session: SessionDep,
    current_user: SuperUser,
    signature_type_in: SignatureTypeCreate,
) -> SignatureType:
    return crud.create_signature_type(
        session=session,
        signature_type_in=signature_type_in,
        owner_id=current_user.id,
    )


@router.put("/{id}", response_model=SignatureTypePublic)
def update_signature_type(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    signature_type_in: SignatureTypeUpdate,
) -> SignatureType:
    obj = crud.get_or_404(session, SignatureType, id)
    return crud.update_obj(session, obj, signature_type_in)


@router.delete("/{id}")
def delete_signature_type(
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
) -> Message:
    obj = crud.get_or_404(session, SignatureType, id)
    session.delete(obj)
    session.commit()
    return Message(message="Signature Type deleted successfully")
