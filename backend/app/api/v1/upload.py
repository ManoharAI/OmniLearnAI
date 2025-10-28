"""
Upload API endpoints for documents, URLs, and videos
"""
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
import logging
import tempfile
import os

logger = logging.getLogger(__name__)

from app.models.response_models import UploadResponse
from app.services.ingestion_service import IngestionService

router = APIRouter()
ingestion_service = IngestionService()

@router.post("/upload/file", response_model=UploadResponse)
async def upload_file(file: UploadFile = File(...)):
    """Upload and process a document file (PDF, DOCX, PPT)"""
    try:
        logger.info(f"Uploading file: {file.filename}")

        # Save file temporarily
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as tmp:
            content = await file.read()
            tmp.write(content)
            tmp_path = tmp.name

        try:
            # Process document
            result = await ingestion_service.process_document(
                file_path=tmp_path,
                filename=file.filename
            )

            # Check if already exists
            if result.get("already_exists"):
                return UploadResponse(
                    source_id=result.get("source_id"),
                    source_type="document",
                    filename=file.filename,
                    status="already_exists",
                    chunks_created=0,
                    message=result.get("message")
                )

            return UploadResponse(
                source_id=result["source_id"],
                source_type="document",
                filename=file.filename,
                status="success",
                chunks_created=result.get("chunks_created", 0)
            )
        finally:
            # Clean up temp file
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)

    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/url", response_model=UploadResponse)
async def upload_url(url: str = Form(...)):
    """Process a web page URL"""
    try:
        logger.info(f"Processing URL: {url}")

        result = await ingestion_service.process_web_url(url)

        # Check if already exists
        if result.get("already_exists"):
            return UploadResponse(
                source_id=result.get("source_id"),
                source_type="web_page",
                filename=url,
                status="already_exists",
                chunks_created=0,
                message=result.get("message")
            )

        return UploadResponse(
            source_id=result["source_id"],
            source_type="web_page",
            filename=result.get("page_title", url),  # Use page title as filename
            status="success",
            chunks_created=result.get("chunks_created", 0),
            metadata={
                "page_title": result.get("page_title", url)
            }
        )

    except Exception as e:
        logger.error(f"URL processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/upload/video", response_model=UploadResponse)
async def upload_video(video_url: str = Form(...)):
    """Process a YouTube video URL"""
    try:
        logger.info(f"Processing video: {video_url}")

        result = await ingestion_service.process_video_url(video_url)

        return UploadResponse(
            source_id=result["source_id"],
            source_type="video",
            filename=result.get("title", video_url),  # Use title as filename
            status="success",
            chunks_created=result.get("chunks_created", 0),
            metadata={
                "title": result.get("title", "Unknown"),
                "channel": result.get("channel", "Unknown"),
                "duration": result.get("duration", "Unknown")
            }
        )

    except Exception as e:
        logger.error(f"Video processing error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
