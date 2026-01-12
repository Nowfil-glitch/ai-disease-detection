import requests

test_image = 'uploads/79242b10ecc8423d9641091fa5b9d874.jpg'

with open(test_image, 'rb') as f:
    files = {'image': ('test.jpg', f, 'image/jpeg')}
    data = {'image_type': 'chest_xray'}
    
    print('Sending analyze request...')
    r = requests.post('http://localhost:8000/api/analyze', files=files, data=data, timeout=120)
    print('Status:', r.status_code)
    if r.status_code == 200:
        result = r.json()
        print('Diagnosis:', result.get('diagnosis'))
        print('Confidence:', result.get('confidence'))
        print('Risk Level:', result.get('risk_level'))
    else:
        print('Error:', r.text)
