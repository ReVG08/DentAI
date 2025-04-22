"""
AI Engine for dental image analysis
Handles communication with OpenAI's API
"""
import base64
from typing import List, Dict, Any, Optional
import io
from PIL import Image

from openai import OpenAI
import config

class DentalAIEngine:
    """Core AI engine that analyzes dental images using OpenAI's API"""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        temperature: float = 0.4,
        max_tokens: int = 1024,
    ):
        """
        Initialize the AI engine with API credentials and configuration.
        """
        self.api_key = api_key or config.OPENAI_API_KEY
        self.model = model or getattr(config, "VISION_MODEL", "gpt-4-vision-preview")
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.client = OpenAI(api_key=self.api_key)

    def _prepare_images(self, images: List[Image.Image]) -> List[str]:
        """Convert images to base64 for API consumption"""
        image_data = []
        for img in images:
            buffered = io.BytesIO()
            img.save(buffered, format="JPEG")
            img_str = base64.b64encode(buffered.getvalue()).decode('utf-8')
            image_data.append(f"data:image/jpeg;base64,{img_str}")
        return image_data

    def analyze_images(
        self,
        images: List[Image.Image],
        patient_info: Dict[str, Any],
        model: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
        language: str = "English"
    ) -> str:
        """
        Analyze dental images to detect issues

        Args:
            images: List of dental images
            patient_info: Dictionary containing patient information
            model: Model to use for analysis (overrides default)
            temperature: Sampling temperature (overrides default)
            max_tokens: Max tokens for response (overrides default)
            language: Output language (default "English")

        Returns:
            Raw analysis string from the AI model
        """
        # Convert images to base64 format
        image_data = self._prepare_images(images)

        # Compose prompt, respecting language
        prompt = (
            f"Analyze these dental images for a patient with the following information:\n"
            f"Age: {patient_info.get('age')}\n"
            f"Gender: {patient_info.get('gender')}\n"
            f"Primary complaint: {patient_info.get('complaint')}\n"
            f"Medical history: {patient_info.get('medical_history')}\n\n"
            f"As a dental expert, identify any issues with the teeth such as:\n"
            f"- Cavities or decay\n"
            f"- Periodontal disease\n"
            f"- Misalignment\n"
            f"- Fractures or cracks\n"
            f"- Infections or abscesses\n"
            f"- Impacted teeth\n"
            f"- Other abnormalities\n\n"
            f"Provide a detailed analysis of what you see in these images."
        )
        if language and language.lower() != "english":
            prompt += f"\nPlease provide the analysis in {language}."

        # Create message content list with patient info and images
        content = [
            {"type": "text", "text": prompt}
        ]
        # Add images to content
        for img_url in image_data:
            content.append({
                "type": "image_url",
                "image_url": {"url": img_url}
            })

        # Make the API call
        try:
            response = self.client.chat.completions.create(
                model=model or self.model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are a highly trained dental professional specialized in diagnostics. "
                            "Analyze dental images carefully, identify issues, and provide detailed findings."
                        ),
                    },
                    {"role": "user", "content": content},
                ],
                temperature=temperature if temperature is not None else self.temperature,
                max_tokens=max_tokens if max_tokens is not None else self.max_tokens,
            )
            return response.choices[0].message.content

        except Exception as e:
            raise AIEngineError(f"Error during image analysis: {str(e)}")

class AIEngineError(Exception):
    """Exception raised for errors in the AI Engine."""
    pass