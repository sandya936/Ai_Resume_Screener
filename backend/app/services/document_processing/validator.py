import re
import hashlib
from typing import Tuple
from fastapi import HTTPException, status
from app.core.config import settings

ALLOWED_EXTENSIONS = {".pdf", ".docx"}
ALLOWED_MIME_TYPES = {
    "application/pdf",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}


def sanitize_filename(filename: str) -> str:
    """Sanitizes user filename to prevent path traversal or injection attacks."""
    # Remove path components (e.g. ../ or c:\)
    clean_name = re.sub(r"^.*[/\\]", "", filename)
    # Allow alphanumeric, hyphen, underscore, dot
    clean_name = re.sub(r"[^\w\.-]", "_", clean_name)
    return clean_name or "resume.pdf"


def calculate_sha256(file_bytes: bytes) -> str:
    return hashlib.sha256(file_bytes).hexdigest()


def validate_resume_file(filename: str, mime_type: str, file_bytes: bytes) -> Tuple[str, str]:
    """
    Validates resume file size, extension, MIME type, magic header bytes, and emptiness.
    Returns (sanitized_filename, sha256_checksum).
    Raises HTTPException if validation fails.
    """
    # 1. Empty check
    if not file_bytes or len(file_bytes) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "EMPTY_FILE",
                    "message": "Uploaded file is empty (0 bytes).",
                    "details": []
                }
            }
        )

    # 2. File size limit check
    if len(file_bytes) > settings.MAX_FILE_SIZE_BYTES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "FILE_TOO_LARGE",
                    "message": f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE_BYTES // (1024 * 1024)}MB.",
                    "details": []
                }
            }
        )

    # 3. Filename sanitization & extension check
    sanitized_name = sanitize_filename(filename)
    ext = "." + sanitized_name.rsplit(".", 1)[-1].lower() if "." in sanitized_name else ""

    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "UNSUPPORTED_EXTENSION",
                    "message": f"Unsupported file extension '{ext}'. Allowed extensions: .pdf, .docx",
                    "details": []
                }
            }
        )

    # 4. MIME type check
    if mime_type and mime_type.lower() not in ALLOWED_MIME_TYPES:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "UNSUPPORTED_MIME_TYPE",
                    "message": f"Unsupported MIME type '{mime_type}'.",
                    "details": []
                }
            }
        )

    # 5. Magic Bytes Header Verification
    if ext == ".pdf":
        if not file_bytes.startswith(b"%PDF-"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "CORRUPTED_FILE",
                        "message": "Invalid PDF file header. The file appears to be corrupted or spoofed.",
                        "details": []
                    }
                }
            )
    elif ext == ".docx":
        if not file_bytes.startswith(b"PK\x03\x04"):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "CORRUPTED_FILE",
                        "message": "Invalid DOCX zip archive header. The file appears to be corrupted or spoofed.",
                        "details": []
                    }
                }
            )

    sha256_checksum = calculate_sha256(file_bytes)
    return sanitized_name, sha256_checksum
