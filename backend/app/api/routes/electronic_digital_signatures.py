import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlmodel import col, func, select

from app.api.deps import CurrentUser, SessionDep
from app.core.files import (
    ALLOWED_CERT_EXT,
    ALLOWED_CERT_TYPES,
    ALLOWED_CONT_EXT,
    ALLOWED_CONT_TYPES,
    delete_upload,
    resolve_upload,
    save_upload,
)
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


def _check_access(sig: ElectronicDigitalSignature, current_user: CurrentUser) -> None:
    if not current_user.is_superuser and sig.owner_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not enough permissions")


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


"""
@router.post("/", response_model=ElectronicDigitalSignaturePublic)
def create_electronic_digital_signature(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    electronic_digital_signature_in: ElectronicDigitalSignatureCreate,
) -> ElectronicDigitalSignature:"""
"""
    Create new electronic digital signature.
    """
"""electronic_digital_signature = ElectronicDigitalSignature.model_validate(
        electronic_digital_signature_in, update={"owner_id": current_user.id}
    )
    session.add(electronic_digital_signature)
    session.commit()
    session.refresh(electronic_digital_signature)
    return electronic_digital_signature
"""


@router.post("/", response_model=ElectronicDigitalSignaturePublic)
async def create_electronic_digital_signature(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    date_certificate: Annotated[datetime, Form()],
    date_container: Annotated[datetime, Form()],
    organization_id: Annotated[uuid.UUID, Form()],
    signature_type_id: Annotated[uuid.UUID, Form()],
    employee_id: Annotated[uuid.UUID, Form()],
    certification_center_id: Annotated[uuid.UUID, Form()],
    file_certificate: Annotated[UploadFile, File()],
    file_container: Annotated[UploadFile, File()],
) -> ElectronicDigitalSignature:
    """
    Create new electronic digital signature with certificate and container files.
    """
    cert_path = await save_upload(
        file_certificate,
        owner_id=current_user.id,
        subdir="certificates",
        allowed_types=ALLOWED_CERT_TYPES,
        allowed_ext=ALLOWED_CERT_EXT,
    )

    try:
        cont_path = await save_upload(
            file_container,
            owner_id=current_user.id,
            subdir="containers",
            allowed_types=ALLOWED_CONT_TYPES,
            allowed_ext=ALLOWED_CONT_EXT,
        )
    except Exception:
        # откатываем первый файл, если второй не сохранился
        delete_upload(cert_path)
        raise

    sig = ElectronicDigitalSignature(
        date_certificate=date_certificate,
        date_container=date_container,
        organization_id=organization_id,
        signature_type_id=signature_type_id,
        employee_id=employee_id,
        certification_center_id=certification_center_id,
        file_certificate=cert_path,
        file_container=cont_path,
        owner_id=current_user.id,
    )

    try:
        session.add(sig)
        session.commit()
        session.refresh(sig)
    except Exception:
        delete_upload(cert_path)
        delete_upload(cont_path)
        raise

    return sig


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
    _ = electronic_digital_signature.sqlmodel_update(update_dict)
    session.add(electronic_digital_signature)
    session.commit()
    session.refresh(electronic_digital_signature)
    return electronic_digital_signature


@router.post("/{id}/certificate", response_model=ElectronicDigitalSignaturePublic)
async def replace_certificate(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    file: Annotated[UploadFile, File()],
) -> ElectronicDigitalSignature:
    """Заменить файл сертификата."""
    sig = session.get(ElectronicDigitalSignature, id)
    if not sig:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    _check_access(sig, current_user)

    old_path = sig.file_certificate
    new_path = await save_upload(
        file,
        owner_id=sig.owner_id,
        subdir="certificates",
        allowed_types=ALLOWED_CERT_TYPES,
        allowed_ext=ALLOWED_CERT_EXT,
    )
    sig.file_certificate = new_path
    session.add(sig)
    session.commit()
    session.refresh(sig)

    delete_upload(old_path)
    return sig


@router.post("/{id}/container", response_model=ElectronicDigitalSignaturePublic)
async def replace_container(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    id: uuid.UUID,
    file: Annotated[UploadFile, File()],
) -> ElectronicDigitalSignature:
    """Заменить файл контейнера."""
    sig = session.get(ElectronicDigitalSignature, id)
    if not sig:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    _check_access(sig, current_user)

    old_path = sig.file_container
    new_path = await save_upload(
        file,
        owner_id=sig.owner_id,
        subdir="containers",
        allowed_types=ALLOWED_CONT_TYPES,
        allowed_ext=ALLOWED_CONT_EXT,
    )
    sig.file_container = new_path
    session.add(sig)
    session.commit()
    session.refresh(sig)

    delete_upload(old_path)
    return sig


@router.get("/{id}/certificate")
def download_certificate(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> FileResponse:
    sig = session.get(ElectronicDigitalSignature, id)
    if not sig:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    _check_access(sig, current_user)

    abs_path = resolve_upload(sig.file_certificate)
    if not abs_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=abs_path,
        filename=f"certificate_{sig.id}{abs_path.suffix}",
        media_type="application/octet-stream",
    )


@router.get("/{id}/container")
def download_container(
    session: SessionDep, current_user: CurrentUser, id: uuid.UUID
) -> FileResponse:
    sig = session.get(ElectronicDigitalSignature, id)
    if not sig:
        raise HTTPException(
            status_code=404, detail="Electronic Digital Signature not found"
        )
    _check_access(sig, current_user)

    abs_path = resolve_upload(sig.file_container)
    if not abs_path.exists():
        raise HTTPException(status_code=404, detail="File not found on disk")

    return FileResponse(
        path=abs_path,
        filename=f"container_{sig.id}{abs_path.suffix}",
        media_type="application/octet-stream",
    )


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
    cert_path = electronic_digital_signature.file_certificate
    cont_path = electronic_digital_signature.file_container
    session.delete(electronic_digital_signature)
    session.commit()
    # файлы удаляем после успешного коммита (best-effort)
    delete_upload(cert_path)
    delete_upload(cont_path)
    return Message(message="Electronic Digital Signature deleted successfully")
