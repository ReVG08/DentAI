"""
AI Engine for dental image analysis.
Handles communication with OpenAI's API.
"""

import base64
from typing import List, Dict, Any, Optional
import io
from PIL import Image
from openai import OpenAI
import config

class DentalAIEngine:
    """Core AI engine for analyzing dental images via OpenAI's API."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.OPENAI_API_KEY
        self.client = OpenAI(api_key=self.api_key)

    @staticmethod
    def _image_to_base64(img: Image.Image) -> str:
        """Convert PIL Image to base64 data URI."""
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
        return f"data:image/jpeg;base64,{img_str}"

    def _prepare_images(self, images: List[Image.Image]) -> List[str]:
        """Convert list of PIL Images to base64 data URIs."""
        return [self._image_to_base64(img) for img in images]

    def analyze_images(self, images: List[Image.Image], patient_info: Dict[str, Any]) -> str:
        """
        Analyze dental images and return AI findings.

        Args:
            images: List of PIL Image objects.
            patient_info: Dict containing patient details.

        Returns:
            Analysis string from the AI model.
        """
        image_data = self._prepare_images(images)
        user_content = [
            {
                "type": "text",
                "text": (
                    f"Analyze these dental images for a patient with the following info:\n"
                    f"Age: {patient_info.get('age', 'N/A')}\n"
                    f"Gender: {patient_info.get('gender', 'N/A')}\n"
                    f"Primary complaint: {patient_info.get('complaint', 'N/A')}\n"
                    f"Medical history: {patient_info.get('medical_history', 'N/A')}\n\n"
                    "As a dental expert, identify any issues such as:\n"
                    "- Cavities/decay\n- Periodontal disease\n- Misalignment\n- Fractures/cracks\n"
                    "- Infections/abscesses\n- Impacted teeth\n- Other abnormalities\n"
                    "Provide a detailed analysis of what you see in these images."
                )
            }
        ] + [
            {"type": "image_url", "image_url": {"url": img_url}}
            for img_url in image_data
        ]

        try:
            response = self.client.chat.completions.create(
                model=config.VISION_MODEL,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a highly trained dental professional specialized in diagnostics. "
                            "Analyze dental images carefully, identify issues, and provide detailed findings and explanations."
                        ),
                    },
                    {"role": "user", "content": user_content},
                ],
                max_tokens=1000
            )
            return response.choices[0].message.content
        except Exception as e:
            raise AIEngineError(f"Error during image analysis: {e}")

class AIEngineError(Exception):
    """Exception for AI Engine errors."""
    pass