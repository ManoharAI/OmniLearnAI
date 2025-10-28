"""
API client for communicating with FastAPI backend
"""
import requests
import os
import streamlit as st
from typing import List, Dict, Optional

class APIClient:
    """Client for GroundRAG FastAPI backend"""

    def __init__(self):
        self.base_url = os.getenv("BACKEND_API_URL", "http://localhost:8000")

    def upload_file(self, file) -> Optional[Dict]:
        """Upload a file to the backend"""
        try:
            st.info(f"🔗 Connecting to: {self.base_url}/api/v1/upload/file")
            files = {"file": (file.name, file.getvalue(), file.type)}
            response = requests.post(
                f"{self.base_url}/api/v1/upload/file",
                files=files,
                timeout=60
            )
            response.raise_for_status()
            result = response.json()
            st.success(f"✅ Backend responded successfully")
            return result
        except requests.exceptions.ConnectionError as e:
            st.error(f"❌ Connection Error: Cannot reach backend at {self.base_url}")
            st.error(f"Details: {str(e)}")
            st.info("💡 Make sure backend is running at http://localhost:8000")
            return None
        except requests.exceptions.Timeout as e:
            st.error(f"⏱️ Timeout: Backend took too long to respond")
            st.error(f"Details: {str(e)}")
            return None
        except requests.exceptions.HTTPError as e:
            st.error(f"❌ HTTP Error: {e.response.status_code}")
            st.error(f"Details: {e.response.text}")
            return None
        except Exception as e:
            st.error(f"❌ Unexpected error: {str(e)}")
            st.error(f"Error type: {type(e).__name__}")
            return None

    def upload_url(self, url: str) -> Optional[Dict]:
        """Process a web URL"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/upload/url",
                data={"url": url},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"URL processing failed: {str(e)}")
            return None

    def upload_video(self, video_url: str) -> Optional[Dict]:
        """Process a video URL"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/upload/video",
                data={"video_url": video_url},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Video processing failed: {str(e)}")
            return None

    def chat(
        self,
        query: str,
        source_ids: List[str],
        chat_history: List[Dict]
    ) -> Dict:
        """Send chat query to backend"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat",
                json={
                    "query": query,
                    "source_ids": source_ids,
                    "chat_history": chat_history
                },
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"Chat failed: {str(e)}")
            return {
                "answer": "Sorry, an error occurred while processing your query.",
                "citations": [],
                "source_ids_used": [],
                "processing_time": 0
            }

    def get_sources(self) -> Optional[Dict]:
        """Get all sources"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/sources",
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            # Silent fail on startup
            return None
    
    def list_sources(self) -> List[Dict]:
        """List all sources"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/sources",
                timeout=30
            )
            response.raise_for_status()
            return response.json().get("sources", [])
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to list sources: {str(e)}")
            return []

    def delete_source(self, source_id: str) -> bool:
        """Delete a source from Qdrant"""
        try:
            response = requests.delete(
                f"{self.base_url}/api/v1/sources/{source_id}",
                timeout=30
            )
            response.raise_for_status()
            return True
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 404:
                st.error("Source not found")
            else:
                st.error(f"Failed to delete: {e.response.text}")
            return False
        except requests.exceptions.RequestException as e:
            st.error(f"Failed to delete source: {str(e)}")
            return False
    
    def get_chat_history(self, source_ids: List[str]) -> Optional[Dict]:
        """Get chat history for specific source combination"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/chat/history",
                json=source_ids,
                timeout=30
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            # Silent fail - no history exists yet
            return None
