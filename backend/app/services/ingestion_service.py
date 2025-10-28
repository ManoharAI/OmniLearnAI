"""
Document ingestion service
"""
from typing import Dict, Any
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, Docx2txtLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import logging
import uuid

from app.config.settings import settings
from app.services.vector_service import VectorStoreManager
from app.db.qdrant_client import check_source_exists

logger = logging.getLogger(__name__)

class IngestionService:
    """Handles ingestion of documents, web pages, and videos"""

    def __init__(self):
        self.vector_manager = VectorStoreManager()
        self.text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=settings.chunk_size,
            chunk_overlap=settings.chunk_overlap
        )

    async def process_document(
        self,
        file_path: str,
        filename: str
    ) -> Dict[str, Any]:
        """Process PDF or DOCX document"""
        try:
            # Check if document already exists
            if check_source_exists(settings.qdrant_collection_documents, filename):
                logger.warning(f"Document already exists: {filename}")
                return {
                    "source_id": None,
                    "chunks_created": 0,
                    "already_exists": True,
                    "message": f"Document '{filename}' already exists in the knowledge base"
                }
            
            # Load document
            if filename.lower().endswith('.pdf'):
                loader = PyPDFLoader(file_path)
            elif filename.lower().endswith('.docx'):
                loader = Docx2txtLoader(file_path)
            else:
                raise ValueError(f"Unsupported file type: {filename}")

            pages = []
            for page in loader.lazy_load():
                pages.append(page)

            # Split into chunks
            chunks = self.text_splitter.split_documents(pages)

            # Prepare documents for vector store
            source_id = str(uuid.uuid4())
            documents = []

            for i, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk.page_content,
                    "metadata": {
                        "source_id": source_id,
                        "source_name": filename,
                        "source_type": "document",
                        "chunk_index": i,
                        "page_number": chunk.metadata.get("page", 0) + 1
                    }
                })

            # Add to vector store
            await self.vector_manager.add_documents(
                settings.qdrant_collection_documents,
                documents
            )

            logger.info(f"Processed document: {filename} ({len(chunks)} chunks)")

            return {
                "source_id": source_id,
                "chunks_created": len(chunks)
            }

        except Exception as e:
            logger.error(f"Error processing document: {str(e)}")
            raise

    def _get_web_page_title(self, url: str, docs: list) -> str:
        """Extract web page title from loaded documents"""
        try:
            # Try to get title from document metadata
            if docs and len(docs) > 0:
                title = docs[0].metadata.get('title', '')
                if title:
                    return title
            
            # Fallback: extract domain name from URL
            from urllib.parse import urlparse
            parsed = urlparse(url)
            domain = parsed.netloc.replace('www.', '')
            return domain if domain else url
            
        except Exception as e:
            logger.warning(f"Could not extract page title: {str(e)}")
            return url

    async def process_web_url(self, url: str) -> Dict[str, Any]:
        """Process web page URL"""
        try:
            # Check if URL already exists
            if check_source_exists(settings.qdrant_collection_web, url):
                logger.warning(f"URL already exists: {url}")
                return {
                    "source_id": None,
                    "chunks_created": 0,
                    "already_exists": True,
                    "message": f"URL '{url}' already exists in the knowledge base"
                }
            
            # Load web page
            loader = WebBaseLoader(url)
            docs = loader.load()

            # Extract page title
            page_title = self._get_web_page_title(url, docs)

            # Split into chunks
            chunks = self.text_splitter.split_documents(docs)

            # Prepare documents
            source_id = str(uuid.uuid4())
            documents = []

            for i, chunk in enumerate(chunks):
                documents.append({
                    "content": chunk.page_content,
                    "metadata": {
                        "source_id": source_id,
                        "source_name": page_title,  # Use page title instead of URL
                        "source_type": "web_page",
                        "chunk_index": i,
                        "url": url
                    }
                })

            # Add to vector store
            await self.vector_manager.add_documents(
                settings.qdrant_collection_web,
                documents
            )

            logger.info(f"Processed web URL: {page_title} ({len(chunks)} chunks)")

            return {
                "source_id": source_id,
                "chunks_created": len(chunks),
                "page_title": page_title
            }

        except Exception as e:
            logger.error(f"Error processing URL: {str(e)}")
            raise

    def _get_video_info(self, video_url: str) -> dict:
        """Extract video title, channel, and info from YouTube URL"""
        try:
            import re
            from urllib.parse import urlparse, parse_qs
            import requests
            
            # Extract video ID
            parsed_url = urlparse(video_url)
            if 'youtube.com' in parsed_url.netloc:
                video_id = parse_qs(parsed_url.query).get('v', [None])[0]
            elif 'youtu.be' in parsed_url.netloc:
                video_id = parsed_url.path.lstrip('/').split('?')[0]
            else:
                return {
                    "title": video_url,
                    "channel": "Unknown",
                    "duration": "Unknown"
                }
            
            if not video_id:
                return {
                    "title": video_url,
                    "channel": "Unknown",
                    "duration": "Unknown"
                }
            
            # Use YouTube oEmbed API (no API key needed)
            oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
            response = requests.get(oembed_url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                title = data.get('title', video_url)
                channel = data.get('author_name', 'Unknown')
                
                # Try to get duration from HTML (basic scraping)
                try:
                    html_response = requests.get(f"https://www.youtube.com/watch?v={video_id}", timeout=5)
                    duration_match = re.search(r'"lengthSeconds":"(\d+)"', html_response.text)
                    if duration_match:
                        seconds = int(duration_match.group(1))
                        minutes = seconds // 60
                        secs = seconds % 60
                        duration = f"{minutes}:{secs:02d}"
                    else:
                        duration = "Unknown"
                except:
                    duration = "Unknown"
                
                return {
                    "title": title,
                    "channel": channel,
                    "duration": duration
                }
            
            return {
                "title": video_url,
                "channel": "Unknown",
                "duration": "Unknown"
            }
            
        except Exception as e:
            logger.warning(f"Could not fetch video info: {str(e)}")
            return {
                "title": video_url,
                "channel": "Unknown",
                "duration": "Unknown"
            }

    async def process_video_url(self, video_url: str) -> Dict[str, Any]:
        """Process YouTube video URL"""
        try:
            # For videos, we store metadata only
            # Actual processing happens via YouTubeVideoUnderstandingTool
            source_id = str(uuid.uuid4())
            
            # Get video info (title, channel, duration)
            video_info = self._get_video_info(video_url)

            documents = [{
                "content": f"YouTube video: {video_url}",
                "metadata": {
                    "source_id": source_id,
                    "source_name": video_info["title"],  # Use title instead of URL
                    "source_type": "video",
                    "video_url": video_url,
                    "duration": video_info["duration"],
                    "channel": video_info["channel"]
                }
            }]

            # Add to vector store
            await self.vector_manager.add_documents(
                settings.qdrant_collection_videos,
                documents
            )

            logger.info(f"Registered video: {video_info['title']} by {video_info['channel']} ({video_url})")

            return {
                "source_id": source_id,
                "chunks_created": 1,
                "duration": video_info["duration"],
                "title": video_info["title"],
                "channel": video_info["channel"]
            }

        except Exception as e:
            logger.error(f"Error processing video: {str(e)}")
            raise
