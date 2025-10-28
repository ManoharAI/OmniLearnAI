"""
Source management service
"""
from typing import List
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

from app.models.response_models import SourceInfo
from app.db.qdrant_client import get_qdrant_client, get_all_sources, delete_source_by_id

class SourceService:
    """Handles source management operations"""

    async def get_all_sources(self) -> List[SourceInfo]:
        """Get all uploaded sources"""
        try:
            all_sources_dict = get_all_sources()
            sources_list = []
            
            for collection_name, sources in all_sources_dict.items():
                for source in sources:
                    # Create base source info
                    source_info = {
                        "source_id": source["source_id"],
                        "source_name": source["source_name"],
                        "source_type": source["source_type"],
                        "chunk_count": source["chunk_count"],
                        "uploaded_at": datetime.now().isoformat(),
                        "metadata": {}
                    }
                    
                    # Add duration and channel for videos
                    if source["source_type"] == "video":
                        if "duration" in source:
                            source_info["metadata"]["duration"] = source["duration"]
                        if "channel" in source:
                            source_info["metadata"]["channel"] = source["channel"]
                    
                    sources_list.append(SourceInfo(**source_info))
            
            return sources_list
        except Exception as e:
            logger.error(f"Error getting sources: {str(e)}")
            return []

    async def get_source(self, source_id: str) -> SourceInfo:
        """Get source by ID"""
        try:
            # Query source from metadata store
            pass
        except Exception as e:
            logger.error(f"Error getting source: {str(e)}")
            return None

    async def delete_source(self, source_id: str):
        """Delete source by ID"""
        try:
            success = delete_source_by_id(source_id)
            if success:
                logger.info(f"Successfully deleted source: {source_id}")
            else:
                logger.warning(f"No documents found for source_id: {source_id}")
                raise ValueError(f"Source {source_id} not found")
        except Exception as e:
            logger.error(f"Error deleting source: {str(e)}")
            raise
