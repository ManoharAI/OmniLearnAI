"""
Audio understanding tool using Gemini API
"""
import os
import mimetypes
import requests
from smolagents import Tool
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class AudioUnderstandingTool(Tool):
    name = "audio_understanding"
    description = (
        """
        A tool to understand and analyze audio using the Gemini API.
        Given one or more audio URLs or local file paths and a text prompt,
        this tool returns Gemini's text response, supporting description,
        summarization, transcription, and Q&A.
        Use this when the user asks about audio files or provides audio URLs.
        """
    )
    inputs = {
        "audios": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "List of audio file URIs or local file paths to process. "
                "Public URLs, HTTP links, or local paths are supported."
            )
        },
        "prompt": {
            "type": "string",
            "description": "Instructions or questions about the audio content."
        }
    }
    output_type = "string"

    def forward(self, audios: list[str], prompt: str) -> str:
        """Analyze audio using Gemini"""
        try:
            # Get API key
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return "Error: GOOGLE_API_KEY not set"

            client = genai.Client(api_key=api_key)
            parts = []

            for audio_ref in audios:
                if audio_ref.startswith("http://") or audio_ref.startswith("https://"):
                    # Fetch from URL
                    resp = requests.get(audio_ref)
                    mime = resp.headers.get('Content-Type', 'audio/mpeg')
                    parts.append(
                        types.Part.from_bytes(data=resp.content, mime_type=mime)
                    )
                else:
                    # Local file
                    with open(audio_ref, 'rb') as f:
                        data = f.read()
                    mime, _ = mimetypes.guess_type(audio_ref)
                    mime = mime or 'application/octet-stream'
                    parts.append(
                        types.Part.from_bytes(data=data, mime_type=mime)
                    )

            # Append prompt at the beginning
            parts.insert(0, types.Part(text=prompt))
            contents = types.Content(parts=parts)

            # Call Gemini API
            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=contents
            )

            logger.info(f"Audio understanding completed for {len(audios)} audio file(s)")
            return response.text

        except Exception as e:
            logger.error(f"Error in audio understanding: {str(e)}")
            return f"Error analyzing audio: {str(e)}"
