"""
Image understanding tool using Gemini API
"""
import os
import mimetypes
import requests
from smolagents import Tool
import google.generativeai as genai
import logging

logger = logging.getLogger(__name__)

class ImageUnderstandingTool(Tool):
    name = "image_understanding"
    description = (
        """
        A tool to understand and analyze images using the Gemini API.
        Given one or more image URLs or local file paths and a text prompt,
        this tool returns Gemini's text response, supporting captioning,
        question-answering, object detection, and more.
        Use this when the user asks about images or provides image URLs.
        """
    )
    inputs = {
        "images": {
            "type": "array",
            "items": {"type": "string"},
            "description": (
                "List of image file URIs or local file paths to process. "
                "Public URLs, HTTP links, or local paths are supported."
            )
        },
        "prompt": {
            "type": "string",
            "description": "Instructions or questions about the image content."
        }
    }
    output_type = "string"

    def forward(self, images: list[str], prompt: str) -> str:
        """Analyze images using Gemini"""
        try:
            # Get API key
            api_key = os.getenv("GOOGLE_API_KEY")
            if not api_key:
                return "Error: GOOGLE_API_KEY not set"

            client = genai.Client(api_key=api_key)
            parts = []

            for img_ref in images:
                # HTTP/HTTPS URL
                if img_ref.startswith("http://") or img_ref.startswith("https://"):
                    resp = requests.get(img_ref)
                    mime = resp.headers.get('Content-Type', 'image/jpeg')
                    parts.append(
                        types.Part.from_bytes(data=resp.content, mime_type=mime)
                    )
                else:
                    # Local file
                    with open(img_ref, 'rb') as f:
                        data = f.read()
                    mime, _ = mimetypes.guess_type(img_ref)
                    mime = mime or 'application/octet-stream'
                    parts.append(
                        types.Part.from_bytes(data=data, mime_type=mime)
                    )

            # Append prompt
            parts.append(types.Part(text=prompt))
            contents = types.Content(parts=parts)

            # Call Gemini API
            response = client.models.generate_content(
                model="models/gemini-2.0-flash",
                contents=contents
            )

            logger.info(f"Image understanding completed for {len(images)} image(s)")
            return response.text

        except Exception as e:
            logger.error(f"Error in image understanding: {str(e)}")
            return f"Error analyzing image: {str(e)}"
