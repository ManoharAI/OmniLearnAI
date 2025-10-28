"""
YouTube video understanding tool using Gemini API
"""
import os
from smolagents import Tool
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class YouTubeVideoUnderstandingTool(Tool):
    name = "youtube_video_understanding"
    description = (
        """
        A tool to understand and analyze YouTube videos using the Gemini API.
        Given a public YouTube URL and a text prompt, this tool returns
        Gemini's text response, supporting summarization, question-answering,
        timestamp references, and transcription.
        Use this when the user asks about YouTube videos or provides YouTube URLs.
        """
    )
    inputs = {
        "youtube_url": {
            "type": "string",
            "description": "Public YouTube video URL to process."
        },
        "prompt": {
            "type": "string",
            "description": "Instructions or questions about the video content."
        }
    }
    output_type = "string"

    def forward(self, youtube_url: str, prompt: str) -> str:
        """Analyze YouTube video using Gemini"""
        try:
            # Get API key
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return "Error: GOOGLE_API_KEY not set"

            # Configure genai
            genai.configure(api_key=api_key)

            # Create model
            model = genai.GenerativeModel('gemini-2.0-flash-exp')

            # Generate content with video URL
            response = model.generate_content([
                youtube_url,
                prompt
            ])

            logger.info(f"Video understanding completed for: {youtube_url}")
            return response.text

        except Exception as e:
            logger.error(f"Error in video understanding: {str(e)}")
            return f"Error analyzing video: {str(e)}"
