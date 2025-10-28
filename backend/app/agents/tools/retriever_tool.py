"""
Retriever tool for semantic search in vector database
"""
from smolagents import Tool
import logging
import asyncio
from typing import TYPE_CHECKING

logger = logging.getLogger(__name__)

if TYPE_CHECKING:
    from app.services.vector_service import VectorStoreManager

class RetrieverTool(Tool):
    name = "retriever"
    description = (
        "Using semantic similarity, retrieves documents from the knowledge "
        "base that have the closest embeddings to the input query. "
        "Returns document content with metadata including page numbers, timestamps, "
        "and source information. Use this tool when the user asks questions about "
        "their uploaded documents or web pages."
    )
    inputs = {
        "query": {
            "type": "string",
            "description": (
                "The query to perform. This should be semantically close "
                "to your target documents. Use affirmative form rather than a question."
            )
        }
    }
    output_type = "string"

    def __init__(self, vector_store_manager: "VectorStoreManager", **kwargs):
        super().__init__(**kwargs)
        self.vector_store_manager = vector_store_manager

    def forward(self, query: str) -> str:
        """Retrieve relevant documents"""
        assert isinstance(query, str), "Query must be a string"

        try:
            # Search across all collections (run async in sync context)
            # Use existing event loop if available (FastAPI context)
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, we need to use run_in_executor
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(
                            asyncio.run,
                            self.vector_store_manager.search_all(query, top_k=10)
                        )
                        results = future.result()
                else:
                    results = loop.run_until_complete(
                        self.vector_store_manager.search_all(query, top_k=10)
                    )
            except RuntimeError:
                # No event loop, create one
                results = asyncio.run(
                    self.vector_store_manager.search_all(query, top_k=10)
                )

            if not results:
                return "No relevant documents found in the knowledge base."

            # Format results with metadata
            formatted_results = "\n\nRetrieved documents:\n"
            for i, result in enumerate(results):
                metadata = result.get("metadata", {})
                source_info = f"Source: {metadata.get('source_name', 'Unknown')}"

                if 'page_number' in metadata:
                    source_info += f", Page: {metadata['page_number']}"
                if 'timestamp' in metadata:
                    source_info += f", Time: {metadata['timestamp']}"

                formatted_results += f"\n===== Document {i} =====\n"
                formatted_results += f"{source_info}\n"
                
                # Include video URL if it's a video
                if metadata.get('source_type') == 'video' and 'video_url' in metadata:
                    formatted_results += f"Video URL: {metadata['video_url']}\n"
                
                formatted_results += f"Content: {result['content'][:500]}...\n"

            logger.info(f"Retrieved {len(results)} documents for query: {query[:50]}...")
            return formatted_results

        except Exception as e:
            logger.error(f"Error in retriever tool: {str(e)}")
            return f"Error retrieving documents: {str(e)}"
