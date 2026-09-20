import io
import re
from typing import List
from fastapi import HTTPException, status
from app.services.document_processing.base import BaseDocumentExtractor
from app.services.document_processing.schemas import NormalizedDocument


class PDFDocumentExtractor(BaseDocumentExtractor):
    def extract(self, file_bytes: bytes, filename: str) -> NormalizedDocument:
        pages_text: List[str] = []
        paragraphs: List[str] = []
        headings: List[str] = []
        bullet_points: List[str] = []
        page_count = 0

        try:
            # 1. Try pypdf (pure Python, DLL-independent)
            try:
                import pypdf
                reader = pypdf.PdfReader(io.BytesIO(file_bytes))
                page_count = len(reader.pages)
                for page in reader.pages:
                    text = page.extract_text() or ""
                    if text.strip():
                        pages_text.append(text)
            except Exception:
                # 2. Fallback to pdfplumber
                import pdfplumber
                with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                    page_count = len(pdf.pages)
                    for page in pdf.pages:
                        text = page.extract_text() or ""
                        if text.strip():
                            pages_text.append(text)

            # Process extracted text lines
            full_raw_text = "\n\n".join(pages_text).strip()
            if full_raw_text:
                lines = [line.strip() for line in full_raw_text.split("\n") if line.strip()]
                for line in lines:
                    if re.match(r"^[\bullet\-\*\u2022\u2023\u25e6\u2043\u2219]\s+", line) or line.startswith("• ") or line.startswith("- "):
                        bullet_points.append(line)
                    elif len(line) < 60 and (line.isupper() or line.endswith(":") or re.match(r"^[A-Z][A-Za-z0-9\s&]{2,30}$", line)):
                        headings.append(line)
                    else:
                        paragraphs.append(line)

        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "EXTRACTION_FAILED",
                        "message": f"Failed to extract text from PDF document: {str(e)}",
                        "details": []
                    }
                }
            )

        ocr_required = False
        if not full_raw_text:
            ocr_required = True
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "EMPTY_DOCUMENT_TEXT",
                        "message": "PDF file contains no readable text (scanned image or empty PDF).",
                        "details": []
                    }
                }
            )

        words = full_raw_text.split()
        word_count = len(words)

        return NormalizedDocument(
            raw_text=full_raw_text,
            word_count=word_count,
            page_count=page_count,
            paragraphs=paragraphs,
            headings=headings,
            bullet_points=bullet_points,
            metadata={
                "extractor": "pypdf",
                "filename": filename,
                "file_type": "pdf"
            },
            ocr_fallback_required=ocr_required
        )
