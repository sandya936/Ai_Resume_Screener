from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field


class NormalizedDocument(BaseModel):
    raw_text: str = Field(..., description="Full extracted plain text string")
    word_count: int = Field(default=0, description="Total word count")
    page_count: int = Field(default=1, description="Total page count")
    paragraphs: List[str] = Field(default_factory=list, description="Extracted paragraphs")
    headings: List[str] = Field(default_factory=list, description="Extracted structural headings")
    bullet_points: List[str] = Field(default_factory=list, description="Extracted bullet point items")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="File and extraction metadata")
    ocr_fallback_required: bool = Field(default=False, description="Flag set if PDF appears to be scanned image")
