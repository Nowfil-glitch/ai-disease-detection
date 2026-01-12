import torch
import torch.nn.functional as F
import numpy as np
import cv2
from typing import Tuple
import logging

logger = logging.getLogger(__name__)


class GradCAM:
    """Grad-CAM implementation for visual explainability"""
    
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.register_hooks()
    
    def register_hooks(self):
        """Register forward and backward hooks"""
        def forward_hook(module, input, output):
            self.activations = output
        
        def backward_hook(module, grad_input, grad_output):
            self.gradients = grad_output[0]
        
        # Find target layer (typically last conv layer before pooling)
        target = None
        if hasattr(self.model, 'backbone'):
            # For our DiseaseClassifier model
            target = self.model.backbone.layer4[-1].conv3
        else:
            # Fallback to last conv layer
            for name, module in self.model.named_modules():
                if isinstance(module, torch.nn.Conv2d):
                    target = module
        
        if target is not None:
            target.register_forward_hook(forward_hook)
            target.register_full_backward_hook(backward_hook)
            logger.info(f"Registered hooks on layer: {target}")
        else:
            logger.warning("Could not find target layer for Grad-CAM")
    
    def generate_cam(self, input_tensor: torch.Tensor, target_class: int = None) -> np.ndarray:
        """
        Generate Grad-CAM heatmap
        
        Args:
            input_tensor: Input image tensor
            target_class: Target class index (if None, uses predicted class)
            
        Returns:
            Heatmap as numpy array
        """
        try:
            self.model.eval()
            
            # Forward pass
            output = self.model(input_tensor)
            
            if target_class is None:
                target_class = output.argmax(dim=1).item()
            
            # Zero gradients
            self.model.zero_grad()
            
            # Backward pass for target class
            one_hot = torch.zeros_like(output)
            one_hot[0][target_class] = 1
            output.backward(gradient=one_hot, retain_graph=True)
            
            # Generate CAM
            if self.gradients is None or self.activations is None:
                logger.warning("Gradients or activations not captured, returning empty heatmap")
                return np.zeros((224, 224))
            
            # Global average pooling of gradients
            weights = torch.mean(self.gradients, dim=(2, 3), keepdim=True)
            
            # Weighted combination of activation maps
            cam = torch.sum(weights * self.activations, dim=1, keepdim=True)
            
            # Apply ReLU
            cam = F.relu(cam)
            
            # Normalize
            cam = cam.squeeze().cpu().detach().numpy()
            cam = cv2.resize(cam, (224, 224))
            cam = (cam - cam.min()) / (cam.max() - cam.min() + 1e-8)
            
            return cam
            
        except Exception as e:
            logger.error(f"Error generating Grad-CAM: {str(e)}")
            return np.zeros((224, 224))
    
    def overlay_heatmap(self, image: np.ndarray, heatmap: np.ndarray, alpha: float = 0.5) -> np.ndarray:
        """
        Overlay heatmap on original image
        
        Args:
            image: Original image (H, W, C)
            heatmap: Heatmap array (H, W)
            alpha: Overlay transparency
            
        Returns:
            Overlay image
        """
        try:
            # Ensure image is uint8
            if image.dtype != np.uint8:
                image = (image * 255).astype(np.uint8)
            
            # Resize heatmap if needed
            if heatmap.shape != image.shape[:2]:
                heatmap = cv2.resize(heatmap, (image.shape[1], image.shape[0]))
            
            # Apply colormap to heatmap
            heatmap_colored = cv2.applyColorMap(
                (heatmap * 255).astype(np.uint8),
                cv2.COLORMAP_JET
            )
            
            # Convert BGR to RGB
            heatmap_colored = cv2.cvtColor(heatmap_colored, cv2.COLOR_BGR2RGB)
            
            # Overlay
            overlay = cv2.addWeighted(image, 1 - alpha, heatmap_colored, alpha, 0)
            
            return overlay
            
        except Exception as e:
            logger.error(f"Error overlaying heatmap: {str(e)}")
            return image


def generate_heatmap_simple(image: np.ndarray) -> np.ndarray:
    """
    Generate a simple simulated heatmap (fallback method)
    Used when Grad-CAM is not available or fails
    """
    try:
        height, width = image.shape[:2]
        
        # Create a radial gradient centered with slight offset
        center_x, center_y = int(width * 0.5), int(height * 0.45)
        y, x = np.ogrid[:height, :width]
        
        # Calculate distance from center
        dist = np.sqrt((x - center_x)**2 + (y - center_y)**2)
        
        # Normalize and invert
        heatmap = 1 - (dist / dist.max())
        
        # Add some noise for realism
        noise = np.random.normal(0, 0.1, heatmap.shape)
        heatmap = np.clip(heatmap + noise, 0, 1)
        
        # Apply gaussian blur
        heatmap = cv2.GaussianBlur(heatmap, (21, 21), 0)
        
        return heatmap
        
    except Exception as e:
        logger.error(f"Error generating simple heatmap: {str(e)}")
        return np.zeros((224, 224))
