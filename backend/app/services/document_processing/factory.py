from fastapi import HTTPException, status
from app.services.document_processing.base import BaseDocumentExtractor
from app.services.document_processing.pdf_extractor import PDFDocumentExtractor
from app.services.document_processing.docx_extractor import DOCXDocumentExtractor


class DocumentProcessorFactory:
    @staticmethod
    def get_extractor(filename: str, mime_type: str = "") -> BaseDocumentExtractor:
        filename_lower = filename.lower()
        if filename_lower.endswith(".pdf") or mime_type == "application/pdf":
            return PDFDocumentExtractor()
        elif filename_lower.endswith(".docx") or mime_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
            return DOCXDocumentExtractor()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "UNSUPPORTED_FORMAT",
                        "message": f"Unsupported document format for filename '{filename}'.",
                        "details": []
                    }
                }
            )
