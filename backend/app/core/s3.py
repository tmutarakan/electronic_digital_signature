import uuid
from pathlib import Path

import boto3
from botocore.client import Config
from fastapi import HTTPException

from app.core.config import settings

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.S3_ENDPOINT,
    aws_access_key_id=settings.S3_ACCESS_KEY,
    aws_secret_access_key=settings.S3_SECRET_KEY,
    region_name=settings.S3_REGION,
    config=Config(
        signature_version="s3v4",
        s3={"addressing_style": "path"} if settings.S3_USE_PATH_STYLE else {},
    ),
)


def ensure_bucket():
    try:
        s3_client.head_bucket(Bucket=settings.S3_BUCKET)
    except Exception:
        s3_client.create_bucket(Bucket=settings.S3_BUCKET)


async def save_upload_s3(file, owner_id, subdir, allowed_types, allowed_ext) -> str:
    """Загружает файл в S3, возвращает ключ объекта."""
    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимый тип файла: {file.content_type}",
        )

    ext = Path(file.filename or "").suffix.lower()
    if ext not in allowed_ext:
        raise HTTPException(
            status_code=400,
            detail=f"Недопустимое расширение: {ext}",
        )
    key = f"{subdir}/{owner_id}/{uuid.uuid4()}{ext}"
    s3_client.upload_fileobj(file.file, settings.S3_BUCKET, key)
    return key


def delete_upload_s3(key: str) -> None:
    s3_client.delete_object(Bucket=settings.S3_BUCKET, Key=key)


def generate_presigned_url(key: str, filename: str, expires: int = 3600) -> str:
    return s3_client.generate_presigned_url(
        "get_object",
        Params={
            "Bucket": settings.S3_BUCKET,
            "Key": key,
            "ResponseContentDisposition": f'attachment; filename="{filename}"',
        },
        ExpiresIn=expires,
    )
