"""
Enhanced image processing module for dental images
Handles preprocessing, normalization, and specialized enhancement for dental imaging
"""
from typing import List, Tuple, Optional, Dict
import io
import numpy as np
from PIL import Image, ImageOps, ImageEnhance, ImageFilter
import cv2

class DentalImageProcessor:
    """Advanced processor for dental images before AI analysis"""
    
    def __init__(self, max_size: Tuple[int, int] = (1024, 1024)):
        """Initialize the image processor with configuration"""
        self.max_size = max_size
        self.supported_formats = ["jpg", "jpeg", "png", "tif", "tiff", "bmp"]
    
    def validate_image(self, image: Image.Image) -> bool:
        """
        Validate if an image is suitable for analysis
        
        Args:
            image: PIL Image object
            
        Returns:
            Boolean indicating if image is valid
        """
        # Check if image format is supported (based on extension)
        format_valid = False
        if hasattr(image, 'format') and image.format:
            format_valid = image.format.lower() in self.supported_formats
        
        # Check minimum dimensions - dental images should have reasonable resolution
        if image.width < 200 or image.height < 200:
            return False
            
        return True
    
    def detect_image_type(self, image: Image.Image) -> str:
        """
        Attempt to detect the type of dental image
        
        Args:
            image: PIL Image object
            
        Returns:
            String indicating image type ('panoramic', 'periapical', 'bitewing', 'intraoral', 'unknown')
        """
        # Convert to numpy for analysis
        img_np = np.array(image.convert('L'))  # Convert to grayscale numpy array
        
        # Calculate aspect ratio
        aspect_ratio = image.width / image.height
        
        # Check for panoramic X-ray (typically wide)
        if aspect_ratio > 2.0:
            return 'panoramic'
        
        # Check for periapical or bitewing X-ray (typically more square)
        elif 0.7 < aspect_ratio < 1.5:
            # Calculate histogram to help distinguish
            hist = cv2.calcHist([img_np], [0], None, [256], [0, 256])
            
            # Check for typical X-ray characteristics (higher contrast)
            if np.std(img_np) > 40:
                # Bitewings typically show both upper and lower teeth
                # This is a simplistic detection and would need refinement
                if np.mean(img_np[0:int(img_np.shape[0]/4)]) < 100 and np.mean(img_np[int(3*img_np.shape[0]/4):]) < 100:
                    return 'bitewing'
                else:
                    return 'periapical'
        
        # Intraoral photos (regular camera photos) typically have color and different characteristics
        if len(np.array(image).shape) == 3:  # Has color channels
            return 'intraoral'
        
        return 'unknown'
    
    def preprocess_image(self, image: Image.Image) -> Image.Image:
        """
        General preprocessing for all dental images
        
        Args:
            image: PIL Image object
            
        Returns:
            Processed PIL Image object
        """
        # Resize if necessary while maintaining aspect ratio
        if image.width > self.max_size[0] or image.height > self.max_size[1]:
            image = ImageOps.contain(image, self.max_size)
        
        # Convert to RGB if not already
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Detect image type for specialized processing
        image_type = self.detect_image_type(image)
        
        # Apply specialized processing based on image type
        if image_type == 'panoramic':
            return self._process_panoramic(image)
        elif image_type == 'periapical':
            return self._process_periapical(image)
        elif image_type == 'bitewing':
            return self._process_bitewing(image)
        elif image_type == 'intraoral':
            return self._process_intraoral(image)
        else:
            # Default processing for unknown types
            return self._default_enhancement(image)
    
    def _process_panoramic(self, image: Image.Image) -> Image.Image:
        """Process panoramic X-ray images"""
        # Convert to grayscale for X-ray processing
        image = image.convert('L')
        
        # Enhance contrast to make features more visible
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.4)
        
        # Apply adaptive histogram equalization (using numpy/cv2)
        img_np = np.array(image)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        img_np = clahe.apply(img_np)
        
        # Convert back to PIL
        image = Image.fromarray(img_np)
        
        # Apply subtle unsharp mask for edge enhancement
        image = image.filter(ImageFilter.UnsharpMask(radius=1.5, percent=150, threshold=3))
        
        # Convert back to RGB for consistent processing
        return image.convert('RGB')
    
    def _process_periapical(self, image: Image.Image) -> Image.Image:
        """Process periapical X-ray images"""
        # Convert to grayscale
        image = image.convert('L')
        
        # Higher contrast for periapical X-rays to highlight root structures
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.5)
        
        # Apply CLAHE with different parameters suited for periapical views
        img_np = np.array(image)
        clahe = cv2.createCLAHE(clipLimit=3.0, tileGridSize=(4, 4))
        img_np = clahe.apply(img_np)
        
        # Convert back to PIL
        image = Image.fromarray(img_np)
        
        # Sharpen to enhance root canal and apex details
        image = image.filter(ImageFilter.SHARPEN)
        image = image.filter(ImageFilter.SHARPEN)  # Apply twice for stronger effect
        
        # Convert back to RGB
        return image.convert('RGB')
    
    def _process_bitewing(self, image: Image.Image) -> Image.Image:
        """Process bitewing X-ray images"""
        # Convert to grayscale
        image = image.convert('L')
        
        # Moderate contrast enhancement
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.3)
        
        # Apply CLAHE with parameters optimized for detecting caries
        img_np = np.array(image)
        clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(6, 6))
        img_np = clahe.apply(img_np)
        
        # Convert back to PIL
        image = Image.fromarray(img_np)
        
        # Apply unsharp mask to enhance edges (good for identifying caries)
        image = image.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=2))
        
        # Convert back to RGB
        return image.convert('RGB')
    
    def _process_intraoral(self, image: Image.Image) -> Image.Image:
        """Process intraoral camera images"""
        # Color balance
        r, g, b = image.split()
        r = ImageEnhance.Brightness(r).enhance(1.05)
        g = ImageEnhance.Brightness(g).enhance(1.0)
        b = ImageEnhance.Brightness(b).enhance(0.95)
        image = Image.merge("RGB", (r, g, b))
        
        # Enhance color saturation slightly
        enhancer = ImageEnhance.Color(image)
        image = enhancer.enhance(1.2)
        
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.15)
        
        # Sharpen for better detail
        image = image.filter(ImageFilter.SHARPEN)
        
        return image
    
    def _default_enhancement(self, image: Image.Image) -> Image.Image:
        """Default image enhancement when type is unknown"""
        # Enhance contrast
        enhancer = ImageEnhance.Contrast(image)
        image = enhancer.enhance(1.2)
        
        # Enhance sharpness
        enhancer = ImageEnhance.Sharpness(image)
        image = enhancer.enhance(1.3)
        
        return image
    
    def process_batch(self, images: List[Image.Image]) -> Dict[str, List]:
        """
        Process a batch of images with type detection and specialized processing
        
        Args:
            images: List of PIL Image objects
            
        Returns:
            Dictionary with processed images and their detected types
        """
        processed_images = []
        image_types = []
        invalid_images = []
        
        for img in images:
            if self.validate_image(img):
                # Detect image type
                img_type = self.detect_image_type(img)
                image_types.append(img_type)
                
                # Process image
                processed_img = self.preprocess_image(img)
                processed_images.append(processed_img)
            else:
                invalid_images.append(img)
        
        return {
            "processed_images": processed_images,
            "image_types": image_types,
            "invalid_images": invalid_images
        }
    
    def save_processed_image(self, image: Image.Image, output_path: str):
        """
        Save processed image to disk
        
        Args:
            image: PIL Image object
            output_path: Path to save the image
        """
        image.save(output_path, quality=95)


class ImageProcessingError(Exception):
    """Exception raised for errors during image processing."""
    pass
