import uuid
from pathlib import Path

from fastapi import HTTPException, UploadFile

from app.core.config import settings

UPLOAD_ROOT = Path(settings.UPLOAD_DIR)

ALLOWED_CERT_TYPES = {
    "application/x-pem-file",
    "application/x-x509-ca-cert",
    "application/pkix-cert",
    "application/octet-stream",
}
ALLOWED_CONT_TYPES = {
    "application/octet-stream",
    "application/zip",
    "application/x-pkcs12",
}

ALLOWED_CERT_EXT = {".pem", ".cer", ".crt", ".der"}
ALLOWED_CONT_EXT = {".zip", ".pfx", ".p12", ".kont"}

MAX_FILE_SIZE = 10 * 1024 * 1024  # 10 MB
CHUNK_SIZE = 1024 * 1024  # 1 MB


async def save_upload(
    file: UploadFile,
    *,
    owner_id: uuid.UUID,
    subdir: str,
    allowed_types: set[str],
    allowed_ext: set[str],
    max_size: int = MAX_FILE_SIZE,
) -> str:
    """
    Сохраняет UploadFile на диск. Возвращает относительный путь для БД.
    """
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый тип файла: {file.content_type}",
        )

    ext = Path(file.filename or "").suffix.lower()
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение файла: {ext or '<нет>'}",
        )

    rel_dir = Path(str(owner_id)) / subdir
    abs_dir = UPLOAD_ROOT / rel_dir
    abs_dir.mkdir(parents=True, exist_ok=True)

    filename = f"{uuid.uuid4().hex}{ext}"
    abs_path = abs_dir / filename
    rel_path = rel_dir / filename

    size = 0
    try:
        with abs_path.open("wb") as out:
            while chunk := await file.read(CHUNK_SIZE):
                size += len(chunk)
                if size > max_size:
                    raise HTTPException(
                        status_code=413,
                        detail=f"Файл слишком большой (>{max_size} байт)",
                    )
                out.write(chunk)
    except HTTPException:
        abs_path.unlink(missing_ok=True)
        raise
    except Exception:
        abs_path.unlink(missing_ok=True)
        raise

    return str(rel_path)


def delete_upload(rel_path: str | None) -> None:
    """Удаляет файл по относительному пути. Best-effort, не бросает исключений."""
    if not rel_path:
        return
    (UPLOAD_ROOT / rel_path).unlink(missing_ok=True)


def resolve_upload(rel_path: str) -> Path:
    """Возвращает абсолютный путь и проверяет, что он внутри UPLOAD_ROOT."""
    abs_path = (UPLOAD_ROOT / rel_path).resolve()
    root = UPLOAD_ROOT.resolve()
    if not str(abs_path).startswith(str(root)):
        raise HTTPException(status_code=400, detail="Некорректный путь к файлу")
    return abs_path
