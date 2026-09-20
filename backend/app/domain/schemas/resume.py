import uuid
from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.services.document_processing.schemas import NormalizedDocument


class ResumeVersionResponse(BaseModel):
    id: uuid.UUID
    resume_id: uuid.UUID
    version_number: int
    filename: str
    file_path: str
    file_size_bytes: int
    mime_type: str
    sha256_checksum: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ResumeResponse(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    title: str
    is_primary: bool
    created_at: datetime
    updated_at: datetime
    versions: List[ResumeVersionResponse] = []

    model_config = ConfigDict(from_attributes=True)


class ExtractedTextResponse(BaseModel):
    resume_id: uuid.UUID
    version_id: uuid.UUID
    status: str
    raw_text: str
    normalized_document: NormalizedDocument
