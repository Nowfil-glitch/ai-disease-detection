#!/usr/bin/env python3
"""
Test script for AI Disease Detection API
"""
import requests
import json
from pathlib import Path

# API Configuration
BASE_URL = "http://localhost:8000"


def test_health_check():
    """Test health check endpoint"""
    print("\n=== Testing Health Check ===")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_root_endpoint():
    """Test root endpoint"""
    print("\n=== Testing Root Endpoint ===")
    response = requests.get(f"{BASE_URL}/")
    print(f"Status Code: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")
    return response.status_code == 200


def test_get_diseases():
    """Test get diseases endpoint"""
    print("\n=== Testing Get Diseases ===")
    response = requests.get(f"{BASE_URL}/api/diseases")
    print(f"Status Code: {response.status_code}")
    if response.status_code == 200:
        data = response.json()
        print(f"Image Types: {list(data['types'].keys())}")
        for image_type, diseases in data['types'].items():
            print(f"\n{image_type}:")
            for disease in diseases[:2]:  # Show first 2
                print(f"  - {disease['name']}")
    return response.status_code == 200


def test_get_diseases_by_type():
    """Test get diseases by type endpoint"""
    print("\n=== Testing Get Diseases by Type ===")
    image_types = ["chest_xray", "bone_xray", "skin_image"]
    
    for image_type in image_types:
        response = requests.get(f"{BASE_URL}/api/diseases/{image_type}")
        print(f"\n{image_type}: Status {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"  Diseases: {len(data['diseases'])}")


def test_analyze_with_sample_image():
    """Test analyze endpoint with a sample image"""
    print("\n=== Testing Analyze Endpoint ===")
    
    # Create a simple test image
    from PIL import Image
    import io
    import numpy as np
    
    # Generate a random test image (simulating medical image)
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    # Make request
    files = {'image': ('test_xray.jpg', img_bytes, 'image/jpeg')}
    data = {'image_type': 'chest_xray'}
    
    print("Uploading test image for analysis...")
    response = requests.post(f"{BASE_URL}/api/analyze", files=files, data=data)
    
    print(f"Status Code: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print(f"\n✓ Analysis Result:")
        print(f"  Diagnosis: {result['diagnosis']}")
        print(f"  Confidence: {result['confidence']:.2%}")
        print(f"  Risk Level: {result['risk_level']}")
        print(f"  Description: {result['description'][:100]}...")
        print(f"  Heatmap URL: {result['heatmap_url']}")
        print(f"  Translations: {list(result['translations'].keys())}")
        return True
    else:
        print(f"Error: {response.text}")
        return False


def test_invalid_file_type():
    """Test with invalid file type"""
    print("\n=== Testing Invalid File Type ===")
    
    # Create a text file
    files = {'image': ('test.txt', b'not an image', 'text/plain')}
    data = {'image_type': 'chest_xray'}
    
    response = requests.post(f"{BASE_URL}/api/analyze", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 400


def test_invalid_image_type():
    """Test with invalid image type"""
    print("\n=== Testing Invalid Image Type ===")
    
    from PIL import Image
    import io
    import numpy as np
    
    img_array = np.random.randint(0, 255, (224, 224, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    
    files = {'image': ('test.jpg', img_bytes, 'image/jpeg')}
    data = {'image_type': 'invalid_type'}
    
    response = requests.post(f"{BASE_URL}/api/analyze", files=files, data=data)
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    return response.status_code == 400


def run_all_tests():
    """Run all tests"""
    print("=" * 60)
    print("AI Disease Detection API - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Health Check", test_health_check),
        ("Root Endpoint", test_root_endpoint),
        ("Get Diseases", test_get_diseases),
        ("Get Diseases by Type", test_get_diseases_by_type),
        ("Analyze Image", test_analyze_with_sample_image),
        ("Invalid File Type", test_invalid_file_type),
        ("Invalid Image Type", test_invalid_image_type)
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"\n❌ Error in {test_name}: {str(e)}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("Test Summary")
    print("=" * 60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✓ PASSED" if result else "✗ FAILED"
        print(f"{status}: {test_name}")
    
    print(f"\nTotal: {passed}/{total} tests passed")
    print("=" * 60)


if __name__ == "__main__":
    print("\nMake sure the API server is running at http://localhost:8000")
    print("Start with: python -m app.main\n")
    
    input("Press Enter to start tests...")
    run_all_tests()
