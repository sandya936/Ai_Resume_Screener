import io
import re
import zipfile
import xml.etree.ElementTree as ET
from typing import List
from fastapi import HTTPException, status
from app.services.document_processing.base import BaseDocumentExtractor
from app.services.document_processing.schemas import NormalizedDocument


class DOCXDocumentExtractor(BaseDocumentExtractor):
    def extract(self, file_bytes: bytes, filename: str) -> NormalizedDocument:
        paragraphs: List[str] = []
        headings: List[str] = []
        bullet_points: List[str] = []
        full_text_list: List[str] = []

        try:
            # 1. Try python-docx if available
            try:
                import docx
                doc = docx.Document(io.BytesIO(file_bytes))
                for p in doc.paragraphs:
                    text = p.text.strip()
                    if not text:
                        continue
                    full_text_list.append(text)
                    style_name = p.style.name if p.style else ""

                    if "Heading" in style_name or (len(text) < 50 and (text.isupper() or text.endswith(":"))):
                        headings.append(text)
                    elif "List" in style_name or re.match(r"^[\bullet\-\*\u2022]\s+", text) or text.startswith("• ") or text.startswith("- "):
                        bullet_points.append(text)
                    else:
                        paragraphs.append(text)
            except Exception:
                # 2. Pure Python zipfile + ElementTree fallback (DLL-independent)
                with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
                    xml_content = z.read("word/document.xml")
                root = ET.fromstring(xml_content)
                ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

                for p_node in root.findall(".//w:p", ns):
                    texts = [node.text for node in p_node.findall(".//w:t", ns) if node.text]
                    p_text = "".join(texts).strip()
                    if not p_text:
                        continue
                    full_text_list.append(p_text)

                    if len(p_text) < 50 and (p_text.isupper() or p_text.endswith(":")):
                        headings.append(p_text)
                    elif re.match(r"^[\bullet\-\*\u2022]\s+", p_text) or p_text.startswith("• ") or p_text.startswith("- "):
                        bullet_points.append(p_text)
                    else:
                        paragraphs.append(p_text)

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "EXTRACTION_FAILED",
                        "message": f"Failed to extract text from DOCX document: {str(e)}",
                        "details": []
                    }
                }
            )

        full_raw_text = "\n\n".join(full_text_list).strip()

        if not full_raw_text:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail={
                    "success": False,
                    "data": None,
                    "error": {
                        "code": "EMPTY_DOCUMENT_TEXT",
                        "message": "DOCX file contains no readable text.",
                        "details": []
                    }
                }
            )

        words = full_raw_text.split()
        word_count = len(words)

        return NormalizedDocument(
            raw_text=full_raw_text,
            word_count=word_count,
            page_count=1,
            paragraphs=paragraphs,
            headings=headings,
            bullet_points=bullet_points,
            metadata={
                "extractor": "zipfile_elementtree",
                "filename": filename,
                "file_type": "docx"
            },
            ocr_fallback_required=False
        )
