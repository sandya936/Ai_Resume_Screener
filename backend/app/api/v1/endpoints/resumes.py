import uuid
from typing import Any, Optional, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload

from app.api.deps import get_db, get_current_active_user, verify_resource_owner
from app.db.models.user import User
from app.db.models.resume import Resume
from app.db.models.resume_version import ResumeVersion
from app.db.models.analysis import Analysis
from app.providers.storage.local import LocalStorageProvider
from app.services.document_processing import (
    validate_resume_file,
    DocumentProcessorFactory,
    NormalizedDocument,
)
from app.domain.schemas.resume import (
    ResumeResponse,
    ResumeVersionResponse,
    ExtractedTextResponse,
)

router = APIRouter()
storage_provider = LocalStorageProvider()


@router.post("/upload", status_code=status.HTTP_201_CREATED)
async def upload_resume(
    file: UploadFile = File(...),
    title: Optional[str] = Form(None),
    resume_id: Optional[str] = Form(None),
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    # 1. Read file bytes
    file_bytes = await file.read()

    # 2. Security & format validation
    sanitized_filename, sha256_checksum = validate_resume_file(
        filename=file.filename or "resume.pdf",
        mime_type=file.content_type or "",
        file_bytes=file_bytes,
    )

    # 3. Extract text & structural entities BEFORE saving or committing
    extractor = DocumentProcessorFactory.get_extractor(
        filename=sanitized_filename, mime_type=file.content_type or ""
    )
    normalized_doc: NormalizedDocument = extractor.extract(file_bytes, sanitized_filename)

    # 4. Save to secure storage
    storage_path = await storage_provider.save_file(
        file_bytes=file_bytes,
        filename=sanitized_filename,
        content_type=file.content_type or "application/octet-stream",
    )

    # 5. Handle parent Resume container
    existing_resume: Optional[Resume] = None
    next_version_num = 1

    if resume_id:
        try:
            r_uuid = uuid.UUID(resume_id)
            result = await db.execute(
                select(Resume).options(selectinload(Resume.versions)).where(Resume.id == r_uuid)
            )
            existing_resume = result.scalar_one_or_none()
            if existing_resume:
                verify_resource_owner(existing_resume.user_id, current_user.id)
                next_version_num = len(existing_resume.versions) + 1
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "INVALID_RESUME_ID",
                        "message": "Invalid resume UUID string format.",
                        "details": [],
                    },
                },
            )

    if not existing_resume:
        resume_title = title or sanitized_filename.rsplit(".", 1)[0].replace("_", " ").title()
        existing_resume = Resume(
            user_id=current_user.id,
            title=resume_title,
            is_primary=True,
        )
        db.add(existing_resume)
        await db.flush()
        next_version_num = 1

    # 6. Create ResumeVersion
    new_version = ResumeVersion(
        resume_id=existing_resume.id,
        version_number=next_version_num,
        filename=sanitized_filename,
        file_path=storage_path,
        file_size_bytes=len(file_bytes),
        mime_type=file.content_type or "application/octet-stream",
        sha256_checksum=sha256_checksum,
    )
    db.add(new_version)
    await db.flush()

    # 7. Save Extraction Analysis Record
    analysis_record = Analysis(
        resume_version_id=new_version.id,
        analysis_type="document_extraction",
        status="completed",
        score=None,
        payload=normalized_doc.model_dump(),
    )
    db.add(analysis_record)
    await db.commit()

    # 8. Re-query full resume model
    result = await db.execute(
        select(Resume).options(selectinload(Resume.versions)).where(Resume.id == existing_resume.id)
    )
    full_resume = result.scalar_one()

    return {
        "success": True,
        "data": {
            "resume": ResumeResponse.model_validate(full_resume),
            "version_id": str(new_version.id),
            "processing_status": "completed",
            "extracted_text_preview": normalized_doc.raw_text[:300] + ("..." if len(normalized_doc.raw_text) > 300 else ""),
            "normalized_document": normalized_doc.model_dump(),
        },
        "error": None,
    }


@router.get("")
async def list_user_resumes(
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(Resume)
        .options(selectinload(Resume.versions))
        .where(Resume.user_id == current_user.id)
        .order_by(Resume.created_at.desc())
    )
    resumes = result.scalars().all()
    return {
        "success": True,
        "data": [ResumeResponse.model_validate(r) for r in resumes],
        "error": None,
    }


@router.get("/{resume_id}")
async def get_resume_by_id(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(Resume).options(selectinload(Resume.versions)).where(Resume.id == resume_id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "RESUME_NOT_FOUND",
                    "message": "Resume record not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(resume.user_id, current_user.id)
    return {
        "success": True,
        "data": ResumeResponse.model_validate(resume),
        "error": None,
    }


@router.get("/versions/{version_id}")
async def get_resume_version_by_id(
    version_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(ResumeVersion)
        .options(selectinload(ResumeVersion.resume))
        .where(ResumeVersion.id == version_id)
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "VERSION_NOT_FOUND",
                    "message": "Resume version not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(version.resume.user_id, current_user.id)
    return {
        "success": True,
        "data": ResumeVersionResponse.model_validate(version),
        "error": None,
    }


@router.get("/versions/{version_id}/extracted-text")
async def get_extracted_text(
    version_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(ResumeVersion)
        .options(selectinload(ResumeVersion.resume), selectinload(ResumeVersion.analyses))
        .where(ResumeVersion.id == version_id)
    )
    version = result.scalar_one_or_none()
    if not version:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "VERSION_NOT_FOUND",
                    "message": "Resume version not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(version.resume.user_id, current_user.id)

    extraction_analysis = next(
        (a for a in version.analyses if a.analysis_type == "document_extraction"), None
    )
    if not extraction_analysis or not extraction_analysis.payload:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "EXTRACTION_NOT_FOUND",
                    "message": "No extracted text analysis found for this version",
                    "details": [],
                },
            },
        )

    norm_doc = NormalizedDocument(**extraction_analysis.payload)

    return {
        "success": True,
        "data": ExtractedTextResponse(
            resume_id=version.resume_id,
            version_id=version.id,
            status=extraction_analysis.status,
            raw_text=norm_doc.raw_text,
            normalized_document=norm_doc,
        ),
        "error": None,
    }


@router.delete("/{resume_id}")
async def delete_resume(
    resume_id: uuid.UUID,
    current_user: User = Depends(get_current_active_user),
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(
        select(Resume).options(selectinload(Resume.versions)).where(Resume.id == resume_id)
    )
    resume = result.scalar_one_or_none()
    if not resume:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "success": False,
                "data": None,
                "error": {
                    "code": "RESUME_NOT_FOUND",
                    "message": "Resume record not found",
                    "details": [],
                },
            },
        )
    verify_resource_owner(resume.user_id, current_user.id)

    # Delete underlying disk files
    for ver in resume.versions:
        await storage_provider.delete_file(ver.file_path)

    await db.delete(resume)
    await db.commit()

    return {
        "success": True,
        "data": {"message": "Resume and all versions successfully deleted"},
        "error": None,
    }
