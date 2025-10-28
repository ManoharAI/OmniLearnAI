"""
API Response Models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class Citation(BaseModel):
    """Citation model"""
    citation_id: int
    source_id: str
    source_name: str
    source_type: str
    location: str  # e.g., "page 5" or "02:34"
    preview_text: str
    confidence_score: Optional[float] = None

class ChatResponse(BaseModel):
    """Chat response model"""
    answer: str
    citations: List[Citation] = []
    source_ids_used: List[str] = []
    processing_time: float

class UploadResponse(BaseModel):
    """Upload response model"""
    source_id: Optional[str] = None
    source_type: str
    filename: str
    status: str
    chunks_created: Optional[int] = None
    upload_time: Optional[datetime] = None
    message: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None  # For video/web metadata

class SourceInfo(BaseModel):
    """Source information model"""
    source_id: str
    source_type: str
    source_name: str
    uploaded_at: str
    chunk_count: int
    metadata: Dict[str, Any] = {}

class SourceListResponse(BaseModel):
    """Source list response"""
    sources: List[SourceInfo]
    total_count: int

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str
    detail: Optional[str] = None
    status_code: int
