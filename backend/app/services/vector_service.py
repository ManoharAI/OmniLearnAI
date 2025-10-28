"""
Vector store service for managing embeddings and search
"""
from typing import List, Dict, Any
from langchain_google_genai import GoogleGenerativeAIEmbeddings
import logging

logger = logging.getLogger(__name__)

from app.config.settings import settings
from app.db.qdrant_client import get_qdrant_client, search_documents, upsert_documents

class VectorStoreManager:
    """Manages vector storage and retrieval across all collections"""

    def __init__(self, source_ids: List[str] = None):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model=settings.embedding_model,
            google_api_key=settings.google_api_key
        )
        self.source_ids = source_ids  # Filter by these source_ids if provided
        logger.info(f"Initialized embeddings: {settings.embedding_model}")
        if source_ids:
            logger.info(f"Filtering by {len(source_ids)} source_ids")

    async def add_documents(
        self,
        collection_name: str,
        documents: List[Dict[str, Any]]
    ) -> List[str]:
        """
        Add documents to vector store

        Args:
            collection_name: Target collection
            documents: List of dicts with 'content' and 'metadata'

        Returns:
            List of document IDs
        """
        try:
            # Extract text content
            texts = [doc["content"] for doc in documents]

            # Generate embeddings
            embeddings = await self.embeddings.aembed_documents(texts)

            # Upsert to Qdrant
            doc_ids = upsert_documents(collection_name, documents, embeddings)

            logger.info(f"Added {len(doc_ids)} documents to {collection_name}")
            return doc_ids

        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise

    async def search(
        self,
        collection_name: str,
        query: str,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """Search in a specific collection"""
        try:
            if top_k is None:
                top_k = settings.retrieval_top_k

            # Generate query embedding
            query_embedding = await self.embeddings.aembed_query(query)

            # Search with source_ids filter if provided
            results = search_documents(
                collection_name=collection_name,
                query_vector=query_embedding,
                top_k=top_k,
                source_ids=self.source_ids
            )

            logger.info(f"Found {len(results)} results in {collection_name}")
            return results

        except Exception as e:
            logger.error(f"Error searching: {str(e)}")
            return []

    async def search_all(
        self,
        query: str,
        top_k: int = None
    ) -> List[Dict[str, Any]]:
        """Search across all collections"""
        collections = [
            settings.qdrant_collection_documents,
            settings.qdrant_collection_web,
            settings.qdrant_collection_videos
        ]

        all_results = []
        for collection in collections:
            results = await self.search(collection, query, top_k)
            all_results.extend(results)

        # Sort by score
        all_results.sort(key=lambda x: x["score"], reverse=True)

        # Return top K
        if top_k:
            all_results = all_results[:top_k]

        return all_results
