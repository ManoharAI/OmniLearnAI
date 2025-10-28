"""
Qdrant vector database client initialization
"""
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct, Filter, FieldCondition, MatchValue
import logging
from typing import List, Dict, Any, Optional
import uuid

logger = logging.getLogger(__name__)

from app.config.settings import settings

qdrant_client = None

def init_qdrant():
    """Initialize Qdrant client and create collections"""
    global qdrant_client

    try:
        qdrant_client = QdrantClient(
            host=settings.qdrant_host,
            port=settings.qdrant_port,
            api_key=settings.qdrant_api_key if settings.qdrant_api_key else None,
            timeout=30.0
        )

        # Test connection
        qdrant_client.get_collections()
        logger.info(f"✅ Connected to Qdrant at {settings.qdrant_host}:{settings.qdrant_port}")

        # Create collections if they don't exist
        collections = [
            settings.qdrant_collection_documents,
            settings.qdrant_collection_web,
            settings.qdrant_collection_videos
        ]

        for collection_name in collections:
            if not qdrant_client.collection_exists(collection_name):
                qdrant_client.create_collection(
                    collection_name=collection_name,
                    vectors_config=VectorParams(
                        size=settings.embedding_dimension,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"📦 Created collection: {collection_name}")
            else:
                logger.info(f"📦 Collection already exists: {collection_name}")

        return qdrant_client

    except Exception as e:
        logger.error(f"❌ Failed to initialize Qdrant: {str(e)}")
        raise

def get_qdrant_client() -> QdrantClient:
    """Get Qdrant client instance"""
    global qdrant_client
    if qdrant_client is None:
        init_qdrant()
    return qdrant_client

def upsert_documents(
    collection_name: str,
    documents: List[Dict[str, Any]],
    embeddings: List[List[float]]
) -> List[str]:
    """
    Upsert documents with embeddings to Qdrant

    Args:
        collection_name: Name of the collection
        documents: List of document dictionaries with content and metadata
        embeddings: List of embedding vectors

    Returns:
        List of document IDs
    """
    client = get_qdrant_client()

    points = []
    doc_ids = []

    for doc, embedding in zip(documents, embeddings):
        doc_id = str(uuid.uuid4())
        doc_ids.append(doc_id)

        point = PointStruct(
            id=doc_id,
            vector=embedding,
            payload={
                "content": doc["content"],
                "metadata": doc.get("metadata", {})
            }
        )
        points.append(point)

    client.upsert(
        collection_name=collection_name,
        points=points
    )

    logger.info(f"✅ Upserted {len(points)} documents to {collection_name}")
    return doc_ids

def search_documents(
    collection_name: str,
    query_vector: List[float],
    top_k: int = 10,
    score_threshold: float = 0.0,
    source_ids: Optional[List[str]] = None
) -> List[Dict[str, Any]]:
    """
    Search for similar documents in Qdrant

    Args:
        collection_name: Name of the collection
        query_vector: Query embedding vector
        top_k: Number of results to return
        score_threshold: Minimum similarity score
        source_ids: Optional list of source_ids to filter by

    Returns:
        List of search results with content, metadata, and scores
    """
    client = get_qdrant_client()

    # Build filter if source_ids provided
    query_filter = None
    if source_ids:
        query_filter = Filter(
            should=[
                FieldCondition(
                    key="metadata.source_id",
                    match=MatchValue(value=source_id)
                )
                for source_id in source_ids
            ]
        )

    results = client.search(
        collection_name=collection_name,
        query_vector=query_vector,
        limit=top_k,
        score_threshold=score_threshold,
        query_filter=query_filter
    )

    formatted_results = []
    for result in results:
        formatted_results.append({
            "id": result.id,
            "score": result.score,
            "content": result.payload["content"],
            "metadata": result.payload.get("metadata", {})
        })

    return formatted_results

def check_source_exists(
    collection_name: str,
    source_name: str
) -> bool:
    """
    Check if a source already exists in the collection
    
    Args:
        collection_name: Name of the collection
        source_name: Name of the source to check
    
    Returns:
        True if source exists, False otherwise
    """
    client = get_qdrant_client()
    
    try:
        # Search for documents with this source_name
        results = client.scroll(
            collection_name=collection_name,
            scroll_filter=Filter(
                must=[
                    FieldCondition(
                        key="metadata.source_name",
                        match=MatchValue(value=source_name)
                    )
                ]
            ),
            limit=1
        )
        
        return len(results[0]) > 0
    except Exception as e:
        logger.error(f"Error checking source existence: {str(e)}")
        return False

def get_all_sources() -> Dict[str, List[Dict[str, Any]]]:
    """
    Get all unique sources from all collections
    
    Returns:
        Dictionary with collection names as keys and list of sources as values
    """
    client = get_qdrant_client()
    all_sources = {}
    
    collections = [
        settings.qdrant_collection_documents,
        settings.qdrant_collection_web,
        settings.qdrant_collection_videos
    ]
    
    for collection_name in collections:
        try:
            if not client.collection_exists(collection_name):
                all_sources[collection_name] = []
                continue
            
            # Get collection info
            collection_info = client.get_collection(collection_name)
            points_count = collection_info.points_count
            
            if points_count == 0:
                all_sources[collection_name] = []
                continue
            
            # Scroll through all points to get unique sources
            sources_map = {}
            offset = None
            
            while True:
                results, offset = client.scroll(
                    collection_name=collection_name,
                    limit=100,
                    offset=offset,
                    with_payload=True,
                    with_vectors=False
                )
                
                if not results:
                    break
                
                for point in results:
                    metadata = point.payload.get("metadata", {})
                    source_name = metadata.get("source_name", "Unknown")
                    source_id = metadata.get("source_id", "unknown")
                    source_type = metadata.get("source_type", "unknown")
                    
                    if source_id not in sources_map:
                        sources_map[source_id] = {
                            "source_id": source_id,
                            "source_name": source_name,
                            "source_type": source_type,
                            "chunk_count": 0
                        }
                        
                        # Add duration and channel for videos
                        if source_type == "video":
                            if "duration" in metadata:
                                sources_map[source_id]["duration"] = metadata["duration"]
                            if "channel" in metadata:
                                sources_map[source_id]["channel"] = metadata["channel"]
                    
                    sources_map[source_id]["chunk_count"] += 1
                
                if offset is None:
                    break
            
            all_sources[collection_name] = list(sources_map.values())
            
        except Exception as e:
            logger.error(f"Error getting sources from {collection_name}: {str(e)}")
            all_sources[collection_name] = []
    
    return all_sources

def delete_source_by_id(source_id: str) -> bool:
    """
    Delete all documents belonging to a source_id from all collections
    
    Args:
        source_id: The source_id to delete
    
    Returns:
        True if deletion was successful, False otherwise
    """
    client = get_qdrant_client()
    
    collections = [
        settings.qdrant_collection_documents,
        settings.qdrant_collection_web,
        settings.qdrant_collection_videos
    ]
    
    deleted_count = 0
    
    for collection_name in collections:
        try:
            if not client.collection_exists(collection_name):
                continue
            
            # Find all points with this source_id
            scroll_result = client.scroll(
                collection_name=collection_name,
                scroll_filter=Filter(
                    must=[
                        FieldCondition(
                            key="metadata.source_id",
                            match=MatchValue(value=source_id)
                        )
                    ]
                ),
                limit=1000,
                with_payload=False,
                with_vectors=False
            )
            
            points_to_delete = [point.id for point in scroll_result[0]]
            
            if points_to_delete:
                client.delete(
                    collection_name=collection_name,
                    points_selector=points_to_delete
                )
                deleted_count += len(points_to_delete)
                logger.info(f"Deleted {len(points_to_delete)} points from {collection_name} for source_id: {source_id}")
        
        except Exception as e:
            logger.error(f"Error deleting from {collection_name}: {str(e)}")
            return False
    
    logger.info(f"Total deleted: {deleted_count} points for source_id: {source_id}")
    return deleted_count > 0
