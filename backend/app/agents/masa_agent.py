"""
MASA Agent setup using smolagents
Based on Kaggle reference implementation
"""
import os
import logging
from smolagents import LiteLLMModel, ToolCallingAgent

logger = logging.getLogger(__name__)

from app.config.settings import settings
from app.agents.tools.retriever_tool import RetrieverTool
from app.agents.tools.image_tool import ImageUnderstandingTool
from app.agents.tools.audio_tool import AudioUnderstandingTool
from app.agents.tools.video_tool import YouTubeVideoUnderstandingTool

# System prompt for the agent
SYSTEM_PROMPT = """You are GroundRAG, a Multi-Source Adaptive Study Agent.
Your goal is to help users by processing their materials from documents, 
web pages, images, audio, and videos, and providing accurate answers 
with proper citations.

You have access to specialized tools for different content types:
- retriever: For searching through uploaded documents, web pages, and videos
- image_understanding: For analyzing images
- audio_understanding: For analyzing audio files
- youtube_video_understanding: For analyzing YouTube videos

IMPORTANT INSTRUCTIONS:
1. You can answer questions using BOTH your general knowledge AND the provided sources
2. When information comes from uploaded sources, cite them with [Source: filename, Page: X]
3. You can provide additional context and explanations beyond the source material
4. If the user says "Strictly Bound" or "Only from sources", then ONLY use the retrieved content
5. Always prioritize source material when available, but feel free to add helpful context
6. Use the 'final_answer' tool to provide your final response

FOR YOUTUBE VIDEOS:
- First use the 'retriever' tool to find the video URL from the knowledge base
- The retriever will return metadata containing the actual video_url
- Extract the video_url from the metadata (look for "YouTube video: https://...")
- Then use 'youtube_video_understanding' tool with the EXACT video_url from the metadata
- DO NOT make up or guess video URLs - always use the URL from the retriever results

Example responses:
- Normal: "Linear algebra studies vectors and matrices [Source: Math.pdf, Page: 5]. It's widely used in machine learning and computer graphics."
- Strictly Bound: "Linear algebra is the study of vectors and matrices [Source: Math.pdf, Page: 5]."
"""

# Global agent instance
_agent = None
_model = None

def get_model():
    """Get or create LLM model instance with retry configuration"""
    global _model
    if _model is None:
        import litellm
        
        # Configure retry settings for 503 errors
        litellm.num_retries = 3  # Retry up to 3 times
        litellm.request_timeout = 60  # 60 second timeout
        
        _model = LiteLLMModel(
            model_id=settings.llm_model,
            temperature=settings.llm_temperature,
            api_key=settings.google_api_key
        )
        logger.info(f"✅ Initialized LLM: {settings.llm_model} (with 3 retries)")
    return _model

def create_agent(vector_store_manager) -> ToolCallingAgent:
    """
    Create agent with all tools

    Args:
        vector_store_manager: Vector store manager for retrieval

    Returns:
        Configured ToolCallingAgent
    """
    global _agent

    # Initialize tools
    retriever_tool = RetrieverTool(vector_store_manager)
    image_tool = ImageUnderstandingTool()
    audio_tool = AudioUnderstandingTool()
    video_tool = YouTubeVideoUnderstandingTool()

    # Create agent
    _agent = ToolCallingAgent(
        tools=[
            retriever_tool,
            image_tool,
            audio_tool,
            video_tool
        ],
        model=get_model()
    )

    # Update system prompt
    _agent.prompt_templates["system_prompt"] = SYSTEM_PROMPT

    logger.info("✅ Created MASA agent with all tools")
    return _agent

def get_agent(vector_store_manager=None) -> ToolCallingAgent:
    """Get or create agent instance with updated vector store manager"""
    if vector_store_manager is None:
        raise ValueError("Vector store manager required for agent initialization")
    
    # Always create a new agent with the provided vector_store_manager
    # This ensures source_ids filtering works correctly
    return create_agent(vector_store_manager)
