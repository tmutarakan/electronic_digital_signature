import uuid
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, HTTPException, File, UploadFile
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.models import (
    ElectronicDigitalSignature,
    ElectronicDigitalSignatureCreate,
    ElectronicDigitalSignaturePublic,
    ElectronicDigitalSignaturesPublic,
    ElectronicDigitalSignatureUpdate,
    Message,
)

router = APIRouter(
    prefix="/electronic-digital-signatures", tags=["electronic-digital-signatures"]
)


@router.get("/", response_model=ElectronicDigitalSignaturesPublic)
def read_electronic_digital_signatures(
    session: SessionDep, current_user: CurrentUser, skip: int = 0, limit: int = 100
) -> ElectronicDigitalSignaturesPublic:
    """
    Retrieve electronic digital signatures.
    """

    if current_user.is_superuser:
        count_statement = select(func.count()).select_from(ElectronicDigitalSignature)
        count = session.exec(count_statement).one()
        statement = (
            select(ElectronicDigitalSignature)
            .order_by(col(ElectronicDigitalSignature.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        electronic_digital_signatures = session.exec(statement).all()
    else:
        count_statement = (
            select(func.count())
            .select_from(ElectronicDigitalSignature)
            .where(ElectronicDigitalSignature.owner_id == current_user.id)
        )
        count = session.exec(count_statement).one()
        statement = (
            select(ElectronicDigitalSignature)
            .where(ElectronicDigitalSignature.owner_id == current_user.id)
            .order_by(col(ElectronicDigitalSignature.created_at).desc())
            .offset(skip)
            .limit(limit)
        )
        electronic_digital_signatures = session.exec(statement).all()

    electronic_digital_signatures_public = [
        ElectronicDigitalSignaturePublic.model_validate(electronic_digital_signature)
        for electronic_digital_signature in electronic_digital_signatures
    ]
    return ElectronicDigitalSignaturesPublic(
        data=electronic_digital_signatures_public, count=count
    )


@router.get("/{id}", response_model=ElectronicDigitalSignaturePublic)
def read_electronic_digital_signature(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> ElectronicDigitalSignature:
    """
    Get electronic digital signature by ID.
    """
    electronic_digital_signature = session.get(ElectronicDigitalSignature, id)
    if not electronic_digital_signature:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    if not current_user.is_superuser and (
        electronic_digital_signature.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    return electronic_digital_signature


@router.post("/", response_model=ElectronicDigitalSignaturePublic)
def create_electronic_digital_signature(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    electronic_digital_signature_in: ElectronicDigitalSignatureCreate,
) -> ElectronicDigitalSignature:
    """
    Create new electronic digital signature.
    """
    electronic_digital_signature = ElectronicDigitalSignature.model_validate(
        electronic_digital_signature_in, update={"owner_id": current_user.id}
    )
    session.add(electronic_digital_signature)
    session.commit()
    session.refresh(electronic_digital_signature)
    return electronic_digital_signature


@router.put("/{id}", response_model=ElectronicDigitalSignaturePublic)
def update_electronic_digital_signature(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    electronic_digital_signature_in: ElectronicDigitalSignatureUpdate,
) -> ElectronicDigitalSignature:
    """
    Update an electronic digital signature.
    """
    electronic_digital_signature = session.get(ElectronicDigitalSignature, id)
    if not electronic_digital_signature:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    if not current_user.is_superuser and (
        electronic_digital_signature.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    update_dict = electronic_digital_signature_in.model_dump(exclude_unset=True)
    _ = electronic_digital_signature.sqlmodel_update(
        update_dict | {"updated_at": datetime.now(ZoneInfo("Europe/Moscow"))}
    )
    session.add(electronic_digital_signature)
    session.commit()
    session.refresh(electronic_digital_signature)
    return electronic_digital_signature


@router.delete("/{id}")
def delete_electronic_digital_signature(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> Message:
    """
    Delete an electronic digital signature.
    """
    electronic_digital_signature = session.get(ElectronicDigitalSignature, id)
    if not electronic_digital_signature:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    if not current_user.is_superuser and (
        electronic_digital_signature.owner_id != current_user.id
    ):
        raise HTTPException(status_code=403, detail="Not enough permissions")
    session.delete(electronic_digital_signature)
    session.commit()
    return Message(message="Electronic Digital Signature deleted successfully")
