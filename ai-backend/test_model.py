#!/usr/bin/env python3
"""
Test script for AI models
"""
import argparse
import torch
from PIL import Image
import numpy as np
from app.models.model_loader import model_manager, DiseaseClassifier
from app.utils.image_processor import image_processor
from app.config import settings
import os


def test_model_loading(model_type: str):
    """Test if model loads correctly"""
    print(f"\n=== Testing Model Loading: {model_type} ===")
    
    try:
        model = model_manager.load_model(model_type)
        print(f"✓ Model loaded successfully")
        print(f"  Device: {model_manager.device}")
        print(f"  Classes: {model_manager.get_class_names(model_type)}")
        return True
    except Exception as e:
        print(f"✗ Failed to load model: {str(e)}")
        return False


def test_model_inference(model_type: str, image_path: str = None):
    """Test model inference"""
    print(f"\n=== Testing Model Inference: {model_type} ===")
    
    try:
        # Create or load test image
        if image_path and os.path.exists(image_path):
            print(f"Using image: {image_path}")
            image_tensor, original = image_processor.preprocess_image(image_path)
        else:
            print("Using random test image")
            # Create random test image
            img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
            
            # Save temporarily
            temp_path = "temp_test_image.jpg"
            img.save(temp_path)
            image_tensor, original = image_processor.preprocess_image(temp_path)
            os.remove(temp_path)
        
        # Run inference
        prediction = model_manager.predict(model_type, image_tensor)
        
        # Get class name
        class_names = model_manager.get_class_names(model_type)
        predicted_class = class_names.get(prediction['predicted_class'], "Unknown")
        
        print(f"✓ Inference successful")
        print(f"  Predicted class: {predicted_class}")
        print(f"  Confidence: {prediction['confidence']:.2%}")
        print(f"  All probabilities:")
        for idx, prob in enumerate(prediction['all_probabilities']):
            class_name = class_names.get(idx, f"Class {idx}")
            print(f"    {class_name}: {prob:.2%}")
        
        return True
        
    except Exception as e:
        print(f"✗ Inference failed: {str(e)}")
        return False


def test_all_models():
    """Test all model types"""
    print("=" * 60)
    print("AI Disease Detection - Model Test Suite")
    print("=" * 60)
    
    model_types = ["chest_xray", "bone_xray", "skin_image"]
    results = []
    
    for model_type in model_types:
        load_result = test_model_loading(model_type)
        inference_result = test_model_inference(model_type)
        results.append((model_type, load_result and inference_result))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    for model_type, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {model_type}")
    
    passed = sum(1 for _, r in results if r)
    print(f"\nTotal: {passed}/{len(results)} models working")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Test AI models")
    parser.add_argument("--model", type=str, choices=["chest_xray", "bone_xray", "skin_image", "all"],
                       default="all", help="Model type to test")
    parser.add_argument("--image", type=str, default=None, help="Path to test image")
    
    args = parser.parse_args()
    
    if args.model == "all":
        test_all_models()
    else:
        test_model_loading(args.model)
        test_model_inference(args.model, args.image)


if __name__ == "__main__":
    main()
