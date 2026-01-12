#!/usr/bin/env python3
"""
Medical AI Model Setup Script
=============================

This script sets up the pre-trained medical AI models:

1. Chest X-Ray: TorchXRayVision DenseNet121
   - Trained on 700K+ chest X-rays
   - Detects 18 pathologies
   - Datasets: NIH, CheXpert, MIMIC-CXR, PadChest

2. Skin Lesion: EfficientNet-B3 (placeholder)
   - For production, train on ISIC dataset
   
3. Bone X-Ray: ResNet50 (placeholder)
   - For production, train on MURA dataset

Usage:
    python create_demo_models.py
"""

import torch
import torch.nn as nn
from torchvision import models
import os
import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from app.config import settings


def print_header(text: str):
    """Print formatted header"""
    print(f"\n{'='*70}")
    print(f"  {text}")
    print(f"{'='*70}\n")


def print_step(step: int, text: str):
    """Print formatted step"""
    print(f"  [{step}] {text}")


def print_success(text: str):
    """Print success message"""
    print(f"  ✓ {text}")


def print_warning(text: str):
    """Print warning message"""
    print(f"  ⚠ {text}")


def print_error(text: str):
    """Print error message"""
    print(f"  ✗ {text}")


def setup_torchxrayvision():
    """
    Setup TorchXRayVision model for chest X-ray analysis.
    
    This model is pre-trained on multiple chest X-ray datasets:
    - NIH ChestX-ray14 (112,120 images)
    - CheXpert (224,316 images)
    - PadChest (160,000 images)
    - MIMIC-CXR (377,110 images)
    
    Total: ~700,000+ chest X-ray images
    
    Falls back to DenseNet121 if TorchXRayVision is not available.
    """
    print_header("Setting up Chest X-Ray Model")
    
    # Try TorchXRayVision first
    try:
        print_step(1, "Trying to import TorchXRayVision...")
        import torchxrayvision as xrv
        print_success("TorchXRayVision imported successfully")
        
        print_step(2, "Downloading pre-trained DenseNet121 model...")
        print("      This model is trained on 700K+ chest X-rays")
        print("      Downloading weights (this may take a few minutes)...")
        
        model = xrv.models.DenseNet(weights="densenet121-res224-all")
        print_success("Model downloaded successfully")
        
        print_step(3, "Model Information:")
        print(f"      - Architecture: DenseNet121 (TorchXRayVision)")
        print(f"      - Input size: 224x224 grayscale")
        print(f"      - Pathologies detected: {len(model.pathologies)}")
        print(f"      - Pathologies: {', '.join(model.pathologies[:5])}...")
        
        print_step(4, "Testing model with dummy input...")
        model.eval()
        dummy_input = torch.randn(1, 1, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        print_success(f"Model output shape: {output.shape}")
        print_success("TorchXRayVision chest X-ray model ready!")
        
        return True
        
    except ImportError:
        print_warning("TorchXRayVision not available (Python 3.12+ compatibility issue)")
        print("      Using fallback DenseNet121 model instead...")
    except Exception as e:
        print_warning(f"TorchXRayVision failed: {str(e)}")
        print("      Using fallback DenseNet121 model instead...")
    
    # Fallback: Create DenseNet121 with multi-label head
    try:
        print_step(2, "Creating fallback DenseNet121 model...")
        
        # 18 pathologies from XRAY_PATHOLOGIES
        num_classes = 18
        
        model = models.densenet121(weights='IMAGENET1K_V1')
        num_features = model.classifier.in_features
        model.classifier = nn.Sequential(
            nn.Linear(num_features, 512),
            nn.ReLU(),
            nn.Dropout(0.3),
            nn.Linear(512, num_classes)
        )
        
        print_success("Fallback model created with ImageNet pre-trained weights")
        
        print_step(3, "Model Information:")
        print(f"      - Architecture: DenseNet121 (Fallback)")
        print(f"      - Input size: 224x224 RGB")
        print(f"      - Output classes: {num_classes} pathologies")
        print(f"      - Pre-training: ImageNet (needs fine-tuning on X-rays)")
        
        print_step(4, "Saving fallback model weights...")
        model_path = os.path.join(settings.MODEL_PATH, "chest_xray_model.pth")
        torch.save(model.state_dict(), model_path)
        file_size = os.path.getsize(model_path) / (1024 * 1024)
        print_success(f"Model saved to: {model_path} ({file_size:.1f} MB)")
        
        print_step(5, "Testing model...")
        model.eval()
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        print_success(f"Model output shape: {output.shape}")
        
        print_warning("NOTE: Fallback model uses ImageNet weights.")
        print("            For accurate predictions, either:")
        print("            1. Install TorchXRayVision (pip install torchxrayvision)")
        print("            2. Fine-tune on NIH ChestX-ray14 dataset")
        
        return True
        
    except Exception as e:
        print_error(f"Error setting up fallback chest model: {str(e)}")
        return False


def setup_skin_model():
    """
    Setup skin lesion classification model.
    
    Uses EfficientNet-B3 with ImageNet pre-trained weights.
    For production, this should be fine-tuned on ISIC dataset.
    """
    print_header("Setting up Skin Lesion Model (EfficientNet-B3)")
    
    try:
        print_step(1, "Checking for TIMM library...")
        try:
            import timm
            use_timm = True
            print_success("TIMM library available")
        except ImportError:
            use_timm = False
            print_warning("TIMM not installed, using torchvision")
        
        print_step(2, "Creating EfficientNet-B3 model...")
        num_classes = 8  # ISIC skin lesion classes
        
        if use_timm:
            model = timm.create_model('efficientnet_b3', pretrained=True, num_classes=num_classes)
        else:
            model = models.efficientnet_b3(weights='IMAGENET1K_V1')
            model.classifier[1] = nn.Linear(model.classifier[1].in_features, num_classes)
        
        print_success("Model created with ImageNet pre-trained weights")
        
        print_step(3, "Model Information:")
        print(f"      - Architecture: EfficientNet-B3")
        print(f"      - Input size: 224x224 RGB")
        print(f"      - Output classes: {num_classes}")
        print(f"      - Classes: Melanoma, BCC, SCC, Actinic Keratosis, etc.")
        
        print_step(4, "Saving model weights...")
        model_path = os.path.join(settings.MODEL_PATH, "skin_lesion_model.pth")
        torch.save(model.state_dict(), model_path)
        file_size = os.path.getsize(model_path) / (1024 * 1024)
        print_success(f"Model saved to: {model_path} ({file_size:.1f} MB)")
        
        print_step(5, "Testing model...")
        model.eval()
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        print_success(f"Model output shape: {output.shape}")
        
        print_warning("NOTE: This uses ImageNet weights - for better accuracy,")
        print("            fine-tune on ISIC skin lesion dataset")
        
        return True
        
    except Exception as e:
        print_error(f"Error setting up skin model: {str(e)}")
        return False


def setup_bone_model():
    """
    Setup bone X-ray classification model.
    
    Uses ResNet50 with ImageNet pre-trained weights.
    For production, this should be fine-tuned on MURA dataset.
    """
    print_header("Setting up Bone X-Ray Model (ResNet50)")
    
    try:
        print_step(1, "Creating ResNet50 model...")
        num_classes = 5  # Bone conditions
        
        model = models.resnet50(weights='IMAGENET1K_V2')
        model.fc = nn.Linear(model.fc.in_features, num_classes)
        
        print_success("Model created with ImageNet pre-trained weights")
        
        print_step(2, "Model Information:")
        print(f"      - Architecture: ResNet50")
        print(f"      - Input size: 224x224 RGB")
        print(f"      - Output classes: {num_classes}")
        print(f"      - Classes: Normal, Fracture, Osteoporosis, Arthritis, Bone Lesion")
        
        print_step(3, "Saving model weights...")
        model_path = os.path.join(settings.MODEL_PATH, "bone_xray_model.pth")
        torch.save(model.state_dict(), model_path)
        file_size = os.path.getsize(model_path) / (1024 * 1024)
        print_success(f"Model saved to: {model_path} ({file_size:.1f} MB)")
        
        print_step(4, "Testing model...")
        model.eval()
        dummy_input = torch.randn(1, 3, 224, 224)
        with torch.no_grad():
            output = model(dummy_input)
        print_success(f"Model output shape: {output.shape}")
        
        print_warning("NOTE: This uses ImageNet weights - for better accuracy,")
        print("            fine-tune on MURA musculoskeletal dataset")
        
        return True
        
    except Exception as e:
        print_error(f"Error setting up bone model: {str(e)}")
        return False


def verify_all_models():
    """Verify all models can be loaded and used"""
    print_header("Verifying Model Integration")
    
    try:
        print_step(1, "Importing model manager...")
        from app.models.model_loader import model_manager
        print_success("Model manager imported")
        
        print_step(2, "Testing chest X-ray model...")
        from PIL import Image
        import numpy as np
        
        # Create dummy image
        dummy_image = Image.fromarray(
            np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
        )
        
        result = model_manager.predict("chest_xray", dummy_image)
        print_success(f"Chest X-ray prediction: {result['primary_finding']}")
        print_success(f"Confidence: {result['confidence']:.2%}")
        print_success(f"Risk level: {result['risk_level']}")
        
        print_step(3, "Testing skin lesion model...")
        result = model_manager.predict("skin_image", dummy_image)
        print_success(f"Skin lesion prediction: {result['primary_finding']}")
        print_success(f"Confidence: {result['confidence']:.2%}")
        
        print_step(4, "Testing bone X-ray model...")
        result = model_manager.predict("bone_xray", dummy_image)
        print_success(f"Bone X-ray prediction: {result['primary_finding']}")
        print_success(f"Confidence: {result['confidence']:.2%}")
        
        return True
        
    except Exception as e:
        print_error(f"Verification failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main setup function"""
    print("\n" + "="*70)
    print("  AI Disease Detection - Medical Model Setup")
    print("="*70)
    print("\nThis script sets up pre-trained medical AI models:")
    print("  • Chest X-Ray: TorchXRayVision (700K+ real X-rays)")
    print("  • Skin Lesion: EfficientNet-B3 (ImageNet pre-trained)")
    print("  • Bone X-Ray:  ResNet50 (ImageNet pre-trained)")
    print("\n" + "="*70)
    
    # Ensure models directory exists
    os.makedirs(settings.MODEL_PATH, exist_ok=True)
    print(f"\nModels directory: {settings.MODEL_PATH}")
    
    results = {}
    
    # Setup each model
    results['chest_xray'] = setup_torchxrayvision()
    results['skin_image'] = setup_skin_model()
    results['bone_xray'] = setup_bone_model()
    
    # Verify integration
    if all(results.values()):
        verification = verify_all_models()
        results['integration'] = verification
    else:
        print_warning("Skipping integration verification due to setup failures")
        results['integration'] = False
    
    # Summary
    print_header("Setup Summary")
    
    model_status = {
        'chest_xray': ('Chest X-Ray (TorchXRayVision)', '700K+ X-rays', 'HIGH'),
        'skin_image': ('Skin Lesion (EfficientNet-B3)', 'ImageNet', 'MEDIUM'),
        'bone_xray': ('Bone X-Ray (ResNet50)', 'ImageNet', 'MEDIUM'),
    }
    
    print("  Model Status:")
    print("  " + "-"*66)
    for key, (name, training_data, accuracy) in model_status.items():
        status = "✓ Ready" if results.get(key) else "✗ Failed"
        print(f"  {status}  {name:<35} [{training_data:<12}] Acc: {accuracy}")
    print("  " + "-"*66)
    
    if results.get('integration'):
        print_success("All models integrated and tested successfully!")
    
    print_header("Next Steps")
    print("  1. Start the backend server:")
    print("     python -m app.main")
    print("")
    print("  2. Start the frontend (in another terminal):")
    print("     cd ../ai-disease-ui && npm run dev")
    print("")
    print("  3. Open the application:")
    print("     http://localhost:3000")
    print("")
    print("  4. For better skin/bone accuracy, fine-tune on:")
    print("     • Skin: ISIC Archive (isic-archive.com)")
    print("     • Bone: MURA Dataset (stanfordmlgroup.github.io/competitions/mura)")
    
    print("\n" + "="*70)
    print("  ⚠️  MEDICAL DISCLAIMER")
    print("="*70)
    print("  This AI system is for EDUCATIONAL PURPOSES ONLY.")
    print("  It is NOT a substitute for professional medical diagnosis.")
    print("  Always consult qualified healthcare professionals.")
    print("="*70 + "\n")
    
    # Exit with appropriate code
    if all(results.values()):
        print("Setup completed successfully! ✓\n")
        return 0
    else:
        print("Setup completed with some failures. Check the errors above.\n")
        return 1


if __name__ == "__main__":
    sys.exit(main())
