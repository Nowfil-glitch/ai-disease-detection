# 🧪 Integration Testing Guide

## Overview

This guide covers testing the integration between the frontend and backend of the AI Disease Detection Platform.

## Prerequisites

- Backend running at http://localhost:8000
- Frontend running at http://localhost:3000
- Demo models created (`python create_demo_models.py`)

## Quick Integration Test

### 1. Test Backend Health

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "AI Disease Detection API"
}
```

### 2. Test API Endpoints

```bash
# Get supported diseases
curl http://localhost:8000/api/diseases

# Get diseases by type
curl http://localhost:8000/api/diseases/chest_xray
```

### 3. Test Image Analysis

Using the API documentation:
1. Open http://localhost:8000/docs
2. Find `POST /api/analyze`
3. Click "Try it out"
4. Upload a test image
5. Set `image_type` to `chest_xray`
6. Execute and verify response

## Frontend Testing

### Manual Testing Steps

1. **Open Frontend**: http://localhost:3000

2. **Upload Test**:
   - Drag and drop an image
   - Or click to browse files
   - Verify image preview appears

3. **Analysis Test**:
   - Click "Analyze Image"
   - Watch console messages appear
   - Wait for results

4. **Results Verification**:
   - Diagnosis displayed
   - Confidence ring animated
   - Heatmap loaded
   - Translations available

5. **Language Test**:
   - Click different language buttons
   - Verify translation text changes

## API Response Format

Expected response from `/api/analyze`:

```json
{
  "diagnosis": "Pneumonia",
  "confidence": 0.92,
  "description": "Pneumonia is an infection that inflames air sacs in one or both lungs.",
  "recommended_action": "⚠️ URGENT: This requires immediate medical attention.",
  "heatmap_url": "http://localhost:8000/static/heatmaps/heatmap_20240101_120000_image.jpg",
  "translations": {
    "en": "Pneumonia detected. Pneumonia is an infection...",
    "hi": "निमोनिया का पता चला...",
    "es": "Se detectó neumonía...",
    "fr": "Pneumonie détectée..."
  },
  "risk_level": "high",
  "disclaimer": "Educational/Informational use only. Not a substitute for professional medical advice."
}
```

## Common Integration Issues

### CORS Errors

**Symptom**: Browser console shows CORS error

**Solution**: Check backend `.env`:
```
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:3001
```

### Network Errors

**Symptom**: "Failed to fetch" in console

**Solutions**:
1. Verify backend is running: `curl http://localhost:8000/health`
2. Check firewall settings
3. Verify correct port numbers

### Heatmap Not Loading

**Symptom**: Heatmap image shows broken icon

**Solutions**:
1. Check `static/heatmaps/` directory exists
2. Verify heatmap URL in response
3. Check file permissions

### Translation Missing

**Symptom**: Only English translation available

**Solutions**:
1. Check internet connection (uses Google Translate API)
2. Verify `deep-translator` is installed
3. Check backend logs for translation errors

## Automated Testing

### Backend Tests

```bash
cd ai-backend
python test_api.py
```

### Test Script Output

```
=== Testing Health Check ===
Status Code: 200
✓ PASSED

=== Testing Analyze Endpoint ===
Status Code: 200
Diagnosis: Pneumonia
Confidence: 85%
✓ PASSED
```

## Performance Benchmarks

| Operation | Expected Time |
|-----------|---------------|
| Image Upload | < 1 second |
| Model Inference | 1-3 seconds |
| Heatmap Generation | 0.5-1 second |
| Translation | 1-2 seconds |
| **Total Analysis** | **3-7 seconds** |

## Checklist

- [ ] Backend starts without errors
- [ ] Frontend starts without errors
- [ ] Health endpoint responds
- [ ] Image upload works
- [ ] Analysis completes successfully
- [ ] Results display correctly
- [ ] Heatmap loads
- [ ] Translations work
- [ ] Language selector functions
- [ ] No console errors

---

⚠️ **Note:** For production testing, use proper medical datasets and validated models.
