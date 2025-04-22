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
    
    def __init__(self, api_key: Optional[str] = None):
        """Initialize the AI engine with API credentials"""
        self.api_key = api_key or config.OPENAI_API_KEY
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
    
    def analyze_images(self, images: List[Image.Image], patient_info: Dict[str, Any]) -> str:
        """
        Analyze dental images to detect issues
        
        Args:
            images: List of dental images
            patient_info: Dictionary containing patient information
            
        Returns:
            Raw analysis string from the AI model
        """
        # Convert images to base64 format
        image_data = self._prepare_images(images)
        
        # Create message content list with patient info and images
        content = [
            {
                "type": "text",
                "text": f"""Analyze these dental images for a patient with the following information:
                Age: {patient_info.get('age')}
                Gender: {patient_info.get('gender')}
                Primary complaint: {patient_info.get('complaint')}
                Medical history: {patient_info.get('medical_history')}
                
                As a dental expert, identify any issues with the teeth such as:
                - Cavities or decay
                - Periodontal disease
                - Misalignment
                - Fractures or cracks
                - Infections or abscesses
                - Impacted teeth
                - Other abnormalities
                
                Provide a detailed analysis of what you see in these images. Do not suggest a consultation with a dentist, as this platform is to speed up a dentist's consulting by pre-diagnosing."""
            }
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
                model=config.VISION_MODEL,
                messages=[
                    {"role": "system", "content": "You are a highly trained dental professional specialized in diagnostics. Analyze dental images carefully, identify issues, and provide detailed findings. Be thorough but avoid making absolute diagnoses that only a dentist can confirm in person."},
                    {"role": "user", "content": content}
                ],
                max_tokens=1000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            raise AIEngineError(f"Error during image analysis: {str(e)}")


class AIEngineError(Exception):
    """Exception raised for errors in the AI Engine."""
    pass
