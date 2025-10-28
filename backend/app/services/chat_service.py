"""
Chat service for processing queries with agentic RAG
"""
from typing import Dict, Any, List
import logging
import re
import time

logger = logging.getLogger(__name__)

from app.services.session_manager import get_session_manager
from app.models.response_models import Citation

class ChatService:
    """Handles chat queries using agentic RAG"""

    def __init__(self):
        self.session_manager = get_session_manager()

    def _extract_citations(self, answer: str) -> List[Citation]:
        """Extract citations from answer text"""
        citations = []

        # Pattern: [Source: filename, Page: X] or [Source: url, Time: XX:XX]
        pattern = r"\[Source: ([^,]+), (?:Page|Time): ([^\]]+)\]"
        matches = re.findall(pattern, answer)

        for i, (source, location) in enumerate(matches, 1):
            citations.append(Citation(
                citation_id=i,
                source_id="",  # Would need to lookup
                source_name=source.strip(),
                source_type="document",  # Would need to determine
                location=location.strip(),
                preview_text="",  # Would need to fetch from vector store
                confidence_score=None
            ))

        return citations

    def _run_agent_with_retry(self, agent, query: str, max_retries: int = 3) -> str:
        """Run agent with retry logic for 503 errors"""
        last_error = None
        
        for attempt in range(max_retries):
            try:
                logger.info(f"Agent attempt {attempt + 1}/{max_retries}")
                result = agent.run(query)
                return result
                
            except Exception as e:
                last_error = e
                error_msg = str(e)
                
                # Check if it's a retryable error (503 or 429)
                if "503" in error_msg or "overloaded" in error_msg.lower() or "429" in error_msg or "rate limit" in error_msg.lower():
                    if attempt < max_retries - 1:
                        # Exponential backoff: 2, 4, 8 seconds
                        wait_time = 2 ** (attempt + 1)
                        logger.warning(f"API overloaded/rate limited. Retrying in {wait_time}s... (attempt {attempt + 1}/{max_retries})")
                        time.sleep(wait_time)
                        continue
                    else:
                        logger.error(f"Max retries reached. Last error: {error_msg}")
                        raise
                else:
                    # Non-retryable error, raise immediately
                    logger.error(f"Non-retryable error: {error_msg}")
                    raise
        
        # If we get here, all retries failed
        raise last_error

    async def process_query(
        self,
        query: str,
        source_ids: List[str],
        chat_history: List[Dict[str, str]]
    ) -> Dict[str, Any]:
        """Process chat query with agentic RAG using session management"""
        try:
            start_time = time.time()
            
            # Check if query requests strict binding
            strictly_bound = any(phrase in query.lower() for phrase in ["strictly bound", "only from sources", "only from source"])
            
            # Get or create session for this source combination
            agent, session_history, session_key = self.session_manager.get_or_create_session(source_ids)

            # Modify query if strictly bound
            if strictly_bound:
                query_to_run = f"{query}\n\nIMPORTANT: Answer ONLY using information from the retrieved sources. Do not add any external knowledge."
            else:
                query_to_run = query

            # Run agent with retry logic
            logger.info(f"Processing query: {query[:100]}... with {len(source_ids) if source_ids else 0} selected sources (Strictly Bound: {strictly_bound})")
            result = self._run_agent_with_retry(agent, query_to_run, max_retries=3)
            
            processing_time = time.time() - start_time

            # Extract citations
            citations = self._extract_citations(result)

            # Add to session history
            self.session_manager.add_to_history(session_key, "user", query)
            self.session_manager.add_to_history(session_key, "assistant", result, citations)

            logger.info(f"Generated answer with {len(citations)} citations (session: {session_key[:8]}...)")

            return {
                "answer": result,
                "citations": citations,
                "source_ids_used": source_ids,
                "session_key": session_key,
                "chat_history": self.session_manager.get_chat_history(session_key),
                "processing_time": processing_time
            }

        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            
            # Check if it's a rate limit or overload error
            error_msg = str(e)
            if "503" in error_msg or "overloaded" in error_msg.lower():
                user_message = "⚠️ The AI model is currently overloaded. I tried 3 times with delays, but it's still unavailable. Please try again in 1-2 minutes."
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                user_message = "⚠️ Rate limit exceeded even after retries. Please wait a moment and try again."
            else:
                user_message = f"I apologize, but I encountered an error: {str(e)}"
            
            return {
                "answer": user_message,
                "citations": [],
                "source_ids_used": source_ids if source_ids else [],
                "chat_history": [],
                "processing_time": 0
            }
