"""
Session manager for maintaining chat sessions and agents per source combination
"""
from typing import Dict, List, Any, Optional, Tuple
import logging
import hashlib
import json

logger = logging.getLogger(__name__)

from app.agents.masa_agent import create_agent
from app.services.vector_service import VectorStoreManager

class SessionManager:
    """Manages chat sessions and agents for different source combinations"""
    
    def __init__(self):
        # Store agents by session_key (hash of sorted source_ids)
        self.agents: Dict[str, Any] = {}
        
        # Store chat history by session_key
        self.chat_histories: Dict[str, List[Dict[str, Any]]] = {}
        
        # Store vector managers by session_key
        self.vector_managers: Dict[str, VectorStoreManager] = {}
        
        logger.info("✅ Initialized SessionManager")
    
    def _get_session_key(self, source_ids: List[str]) -> str:
        """
        Generate a unique session key for a combination of source_ids
        
        Args:
            source_ids: List of source IDs
        
        Returns:
            Hash string representing this source combination
        """
        if not source_ids:
            return "all_sources"
        
        # Sort to ensure same sources in different order get same key
        sorted_ids = sorted(source_ids)
        key_string = json.dumps(sorted_ids)
        return hashlib.md5(key_string.encode()).hexdigest()
    
    def get_or_create_session(
        self, 
        source_ids: List[str]
    ) -> Tuple[Any, List[Dict[str, Any]], str]:
        """
        Get existing session or create new one for source combination
        
        Args:
            source_ids: List of source IDs to chat with
        
        Returns:
            Tuple of (agent, chat_history, session_key)
        """
        session_key = self._get_session_key(source_ids)
        
        # Check if session exists
        if session_key in self.agents:
            logger.info(f"♻️ Reusing existing session: {session_key[:8]}... ({len(source_ids)} sources)")
            return (
                self.agents[session_key],
                self.chat_histories[session_key],
                session_key
            )
        
        # Create new session
        logger.info(f"🆕 Creating new session: {session_key[:8]}... ({len(source_ids)} sources)")
        
        # Create vector manager with source filter
        vector_manager = VectorStoreManager(source_ids=source_ids if source_ids else None)
        self.vector_managers[session_key] = vector_manager
        
        # Create agent
        agent = create_agent(vector_manager)
        self.agents[session_key] = agent
        
        # Initialize empty chat history
        self.chat_histories[session_key] = []
        
        return agent, self.chat_histories[session_key], session_key
    
    def add_to_history(
        self, 
        session_key: str, 
        role: str, 
        content: str,
        citations: List[Any] = None
    ):
        """
        Add message to session's chat history
        
        Args:
            session_key: Session identifier
            role: 'user' or 'assistant'
            content: Message content
            citations: Optional citations for assistant messages
        """
        if session_key not in self.chat_histories:
            self.chat_histories[session_key] = []
        
        message = {
            "role": role,
            "content": content
        }
        
        if citations:
            message["citations"] = citations
        
        self.chat_histories[session_key].append(message)
        logger.info(f"Added {role} message to session {session_key[:8]}...")
    
    def get_chat_history(self, session_key: str) -> List[Dict[str, Any]]:
        """Get chat history for a session"""
        return self.chat_histories.get(session_key, [])
    
    def clear_session(self, session_key: str):
        """Clear a specific session"""
        if session_key in self.agents:
            del self.agents[session_key]
        if session_key in self.chat_histories:
            del self.chat_histories[session_key]
        if session_key in self.vector_managers:
            del self.vector_managers[session_key]
        logger.info(f"🗑️ Cleared session: {session_key[:8]}...")
    
    def clear_all_sessions(self):
        """Clear all sessions"""
        self.agents.clear()
        self.chat_histories.clear()
        self.vector_managers.clear()
        logger.info("🗑️ Cleared all sessions")
    
    def get_active_sessions(self) -> List[Dict[str, Any]]:
        """Get list of active sessions"""
        sessions = []
        for session_key in self.agents.keys():
            sessions.append({
                "session_key": session_key,
                "message_count": len(self.chat_histories.get(session_key, []))
            })
        return sessions

# Global session manager instance
_session_manager = None

def get_session_manager() -> SessionManager:
    """Get or create global session manager"""
    global _session_manager
    if _session_manager is None:
        _session_manager = SessionManager()
    return _session_manager
