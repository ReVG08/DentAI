"""
Image processing module for dental images
Handles image validation, preprocessing, and optimization
"""
from typing import List, Tuple
import io
from PIL import Image, ImageOps, ImageEnhance

import app.config as config

class ImageProcessor:
    """Processes dental images before AI analysis"""
    
    def __init__(self, max_size: Tuple[int, int] = None):
        """Initialize the image processor with configuration"""
        self.max_size = max_size or config.MAX_IMAGE_SIZE
        self.supported_formats = config.SUPPORTED_FORMATS
    
    def validate_image(self, image: Image.Image) -> bool:
        """
        Validate if an image is suitable for analysis
        
        Args:
            image: PIL Image object
            
        Returns:
            Boolean indicating if image is valid
        """
        # Check if image format is supported
        if image.format and image.format.lower() not in self.supported_formats:
            return False
            
        # Check minimum dimensions
        if image.width < 200 or image.height < 200:
            return False
            
        return True
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        Preprocess image for optimal AI analysis
        
        Args:
            image: PIL Image object
            
        Returns:
            Processed PIL Image object
        """
        # Resize if necessary
        if image.width > self.max_size[0] or image.height > self.max_size[1]:
            image = ImageOps.contain(image, self.max_size)
        
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Enhance contrast slightly for better feature detection
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance sharpness for better edge detection
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        return image
    
    def process_batch(self, images: List[Image.Image]) -> List[Image.Image]:
        """
        Process a batch of images
        
        Args:
            images: List of PIL Image objects
            
        Returns:
            List of processed PIL Image objects
        """
        processed_images = []
        
        for img in images:
            if self.validate_image(img):
                processed_img = self.preprocess_image(img)
                processed_images.append(processed_img)
        
        return processed_images


class ImageProcessingError(Exception):
    """Exception raised for errors during image processing."""
    pass