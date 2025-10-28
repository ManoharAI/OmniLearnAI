"""
Sources API endpoints for managing uploaded sources
"""
from fastapi import APIRouter, HTTPException
import logging

logger = logging.getLogger(__name__)

from app.models.response_models import SourceListResponse, SourceInfo
from app.services.source_service import SourceService

router = APIRouter()
source_service = SourceService()

@router.get("/sources", response_model=SourceListResponse)
async def list_sources():
    """List all uploaded sources"""
    try:
        sources = await source_service.get_all_sources()
        return SourceListResponse(
            sources=sources,
            total_count=len(sources)
        )
    except Exception as e:
        logger.error(f"Error listing sources: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/sources/{source_id}")
async def delete_source(source_id: str):
    """Delete a source by ID"""
    try:
        await source_service.delete_source(source_id)
        return {"status": "success", "message": f"Deleted source {source_id}"}
    except Exception as e:
        logger.error(f"Error deleting source: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/sources/{source_id}", response_model=SourceInfo)
async def get_source(source_id: str):
    """Get source details by ID"""
    try:
        source = await source_service.get_source(source_id)
        if not source:
            raise HTTPException(status_code=404, detail="Source not found")
        return source
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting source: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
