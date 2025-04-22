"""
Image processing module for dental images.
Handles image validation, preprocessing, and optimization.
"""

from typing import List, Tuple, Optional
import io
from PIL import Image, ImageOps, ImageEnhance
import config

class ImageProcessor:
    """Processes dental images for optimal AI analysis."""

    def __init__(self, max_size: Optional[Tuple[int, int]] = None, supported_formats: Optional[List[str]] = None):
        self.max_size = max_size or config.MAX_IMAGE_SIZE
        self.supported_formats = [fmt.lower() for fmt in (supported_formats or config.SUPPORTED_FORMATS)]

    def validate_image(self, image: Image.Image) -> bool:
        """
        Validate if an image is suitable for analysis.
        Returns True if valid, else False.
        """
        fmt = (image.format or '').lower()
        if fmt not in self.supported_formats:
            return False
        if image.width < 200 or image.height < 200:
            return False
        return True

    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for optimal AI analysis.
        Returns a processed PIL Image.
        """
        img = image.copy()
        # Resize if necessary
        if img.width > self.max_size[0] or img.height > self.max_size[1]:
            img = ImageOps.contain(img, self.max_size)
        # Convert to RGB
        if img.mode != 'RGB':
            img = img.convert('RGB')
        # Enhance contrast
        img = ImageEnhance.Contrast(img).enhance(1.2)
        # Enhance sharpness
        img = ImageEnhance.Sharpness(img).enhance(1.3)
        return img

    def process_batch(self, images: List[Image.Image]) -> List[Image.Image]:
        """
        Validate and preprocess a batch of images.
        Returns a list of processed PIL Images.
        """
        return [self.preprocess_image(img) for img in images if self.validate_image(img)]

class ImageProcessingError(Exception):
    """Exception for errors during image processing."""
    pass