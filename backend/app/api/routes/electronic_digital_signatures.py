import uuid
from datetime import datetime
from typing import Annotated

from fastapi import APIRouter, File, Form, UploadFile
from sqlmodel import Session

from app import crud
from app.api.deps import CurrentUser, SessionDep, SuperUser
from app.core.files import (
    ALLOWED_CERT_EXT,
    ALLOWED_CERT_TYPES,
    ALLOWED_CONT_EXT,
    ALLOWED_CONT_TYPES,
)
from app.core.s3 import delete_upload_s3, save_upload_s3
from app.models import (
    ElectronicDigitalSignature,
    ElectronicDigitalSignaturePublic,
    ElectronicDigitalSignaturesPublic,
    ElectronicDigitalSignatureUpdate,
    Message,
)

router = APIRouter(
    prefix="/electronic-digital-signatures",
    tags=["electronic-digital-signatures"],
)


# ---------- чтение: все аутентифицированные ----------


@router.get("/", response_model=ElectronicDigitalSignaturesPublic)
def read_electronic_digital_signatures(
    session: SessionDep,
    _current_user: CurrentUser,
    skip: int = 0,
    limit: int = 100,
) -> ElectronicDigitalSignaturesPublic:
    """
    Retrieve electronic digital signatures.
    Доступно всем аутентифицированным пользователям.
    """
    items, count = crud.list_all(session, ElectronicDigitalSignature, skip, limit)
    return ElectronicDigitalSignaturesPublic(
        data=[ElectronicDigitalSignaturePublic.model_validate(x) for x in items],
        count=count,
    )


@router.get("/{id}", response_model=ElectronicDigitalSignaturePublic)
def read_electronic_digital_signature(
    session: SessionDep,
    _current_user: CurrentUser,
    id: uuid.UUID,
) -> ElectronicDigitalSignature:
    """
    Get electronic digital signature by ID.
    Доступно всем аутентифицированным пользователям.
    """
    return crud.get_or_404(session, ElectronicDigitalSignature, id)


# ---------- создание: только суперпользователь, с S3 ----------


@router.post("/", response_model=ElectronicDigitalSignaturePublic)
async def create_electronic_digital_signature(
    *,
    session: SessionDep,
    current_user: SuperUser,
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
    Только для суперпользователя.

    Логика с S3 остаётся в роутере: сначала грузим оба файла,
    потом создаём запись, при падении — откатываем.
    """
    cert_path = await save_upload_s3(
        file_certificate,
        owner_id=current_user.id,
        subdir="certificates",
        allowed_types=ALLOWED_CERT_TYPES,
        allowed_ext=ALLOWED_CERT_EXT,
    )

    try:
        cont_path = await save_upload_s3(
            file_container,
            owner_id=current_user.id,
            subdir="containers",
            allowed_types=ALLOWED_CONT_TYPES,
            allowed_ext=ALLOWED_CONT_EXT,
        )
    except Exception:
        delete_upload_s3(cert_path)
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
        owner_id=current_user.id,  # аудит
    )

    try:
        session.add(sig)
        session.commit()
        session.refresh(sig)
    except Exception:
        delete_upload_s3(cert_path)
        delete_upload_s3(cont_path)
        raise

    return sig


# ---------- обновление метаданных: только суперпользователь ----------


@router.put("/{id}", response_model=ElectronicDigitalSignaturePublic)
def update_electronic_digital_signature(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    electronic_digital_signature_in: ElectronicDigitalSignatureUpdate,
) -> ElectronicDigitalSignature:
    """
    Update an electronic digital signature (метаданные, без файлов).
    Только для суперпользователя.
    """
    sig = crud.get_or_404(session, ElectronicDigitalSignature, id)
    return crud.update_obj(session, sig, electronic_digital_signature_in)


# ---------- замена файлов: только суперпользователь ----------


@router.post("/{id}/certificate", response_model=ElectronicDigitalSignaturePublic)
async def replace_certificate(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    file: Annotated[UploadFile, File()],
) -> ElectronicDigitalSignature:
    """Заменить файл сертификата. Только для суперпользователя."""
    sig = crud.get_or_404(session, ElectronicDigitalSignature, id)
    return await _replace_file(
        session=session,
        sig=sig,
        file=file,
        field="file_certificate",
        subdir="certificates",
        allowed_types=ALLOWED_CERT_TYPES,
        allowed_ext=ALLOWED_CERT_EXT,
    )


@router.post("/{id}/container", response_model=ElectronicDigitalSignaturePublic)
async def replace_container(
    *,
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
    file: Annotated[UploadFile, File()],
) -> ElectronicDigitalSignature:
    """Заменить файл контейнера. Только для суперпользователя."""
    sig = crud.get_or_404(session, ElectronicDigitalSignature, id)
    return await _replace_file(
        session=session,
        sig=sig,
        file=file,
        field="file_container",
        subdir="containers",
        allowed_types=ALLOWED_CONT_TYPES,
        allowed_ext=ALLOWED_CONT_EXT,
    )


# ---------- удаление: только суперпользователь, с удалением файлов ----------


@router.delete("/{id}")
def delete_electronic_digital_signature(
    session: SessionDep,
    _current_user: SuperUser,
    id: uuid.UUID,
) -> Message:
    """
    Delete an electronic digital signature вместе с файлами в S3.
    Только для суперпользователя.
    """
    sig = crud.get_or_404(session, ElectronicDigitalSignature, id)
    cert_path = sig.file_certificate
    cont_path = sig.file_container
    session.delete(sig)
    session.commit()
    # файлы удаляем после успешного коммита (best-effort)
    delete_upload_s3(cert_path)
    delete_upload_s3(cont_path)
    return Message(message="Electronic Digital Signature deleted successfully")


# ---------- внутренний хелпер роутера ----------


async def _replace_file(
    *,
    session: Session,
    sig: ElectronicDigitalSignature,
    file: UploadFile,
    field: str,
    subdir: str,
    allowed_types: set[str],
    allowed_ext: set[str],
) -> ElectronicDigitalSignature:
    """
    Общая логика замены файла: сохранить новый → обновить запись → удалить старый.
    При падении коммита удаляет новый файл, чтобы не оставлять мусор в S3.
    """
    old_path: str = getattr(sig, field)

    new_path = await save_upload_s3(
        file,
        owner_id=sig.owner_id,
        subdir=subdir,
        allowed_types=allowed_types,
        allowed_ext=allowed_ext,
    )
    setattr(sig, field, new_path)
    session.add(sig)

    try:
        session.commit()
        session.refresh(sig)
    except Exception:
        delete_upload_s3(new_path)
        raise

    delete_upload_s3(old_path)
    return sig
