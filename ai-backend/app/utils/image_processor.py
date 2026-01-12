import torch
import numpy as np
from PIL import Image
import cv2
from torchvision import transforms
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class ImageProcessor:
    """Image preprocessing and handling utilities"""
    
    def __init__(self):
        # Standard ImageNet normalization for pre-trained models
        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])
        
        # Transform without normalization for visualization
        self.transform_no_norm = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor()
        ])
    
    def preprocess_image(self, image_path: str) -> Tuple[torch.Tensor, np.ndarray]:
        """
        Preprocess image for model inference
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (preprocessed_tensor, original_image_array)
        """
        try:
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Store original for visualization
            original = np.array(image.resize((224, 224)))
            
            # Preprocess for model
            image_tensor = self.transform(image)
            image_tensor = image_tensor.unsqueeze(0)  # Add batch dimension
            
            logger.info(f"Image preprocessed successfully: {image_tensor.shape}")
            return image_tensor, original
            
        except Exception as e:
            logger.error(f"Error preprocessing image: {str(e)}")
            raise
    
    def validate_image(self, image_path: str) -> bool:
        """Validate if file is a valid image"""
        try:
            img = Image.open(image_path)
            img.verify()
            return True
        except Exception as e:
            logger.warning(f"Invalid image file: {str(e)}")
            return False
    
    def get_image_info(self, image_path: str) -> dict:
        """Get image metadata"""
        try:
            img = Image.open(image_path)
            return {
                "format": img.format,
                "mode": img.mode,
                "size": img.size,
                "width": img.width,
                "height": img.height
            }
        except Exception as e:
            logger.error(f"Error getting image info: {str(e)}")
            return {}


image_processor = ImageProcessor()
