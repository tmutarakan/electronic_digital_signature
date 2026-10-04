from pathlib import Path

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
