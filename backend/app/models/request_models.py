"""
API Request Models
"""
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

class ChatRequest(BaseModel):
    """Chat request model"""
    query: str = Field(..., description="User query")
    source_ids: List[str] = Field(
        default=[],
        description="List of source IDs to query (empty = all sources)"
    )
    chat_history: List[Dict[str, str]] = Field(
        default=[],
        description="Chat history for context"
    )

class UploadURLRequest(BaseModel):
    """URL upload request"""
    url: str = Field(..., description="Web page or video URL")

class SourceFilterRequest(BaseModel):
    """Source filter request"""
    source_types: Optional[List[str]] = Field(
        default=None,
        description="Filter by source types: document, web_page, video"
    )
    search_query: Optional[str] = Field(
        default=None,
        description="Search query to filter sources"
    )
