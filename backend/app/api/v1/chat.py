"""
Chat API endpoint for agentic RAG queries
"""
from fastapi import APIRouter, HTTPException, Body
import logging
import time
from typing import List

logger = logging.getLogger(__name__)

from app.models.request_models import ChatRequest
from app.models.response_models import ChatResponse
from app.services.chat_service import ChatService
from app.services.session_manager import get_session_manager

router = APIRouter()
chat_service = ChatService()

@router.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Process chat query using agentic RAG"""
    try:
        start_time = time.time()

        logger.info(f"Chat query: {request.query[:100]}...")

        # Process query
        result = await chat_service.process_query(
            query=request.query,
            source_ids=request.source_ids,
            chat_history=request.chat_history
        )

        processing_time = time.time() - start_time

        return ChatResponse(
            answer=result["answer"],
            citations=result.get("citations", []),
            source_ids_used=result.get("source_ids_used", []),
            processing_time=processing_time
        )

    except Exception as e:
        logger.error(f"Chat error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/chat/history")
async def get_chat_history(source_ids: List[str] = Body(...)):
    """Get chat history for a specific source combination"""
    try:
        session_manager = get_session_manager()
        session_key = session_manager._get_session_key(source_ids)
        history = session_manager.get_chat_history(session_key)
        
        return {
            "session_key": session_key,
            "chat_history": history,
            "message_count": len(history)
        }
    except Exception as e:
        logger.error(f"Error getting chat history: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
