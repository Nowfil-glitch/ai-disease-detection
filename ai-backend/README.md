# AI Disease Detection Backend API

A FastAPI backend for AI-powered medical image analysis.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Install dependencies
pip install -r requirements.txt

# Create demo models
python create_demo_models.py

# Run server
python -m app.main
```

## API Endpoints

- `POST /api/analyze` - Analyze medical image
- `GET /api/diseases` - Get supported diseases
- `GET /health` - Health check
- `GET /docs` - API documentation

## URLs

- API: http://localhost:8000
- Docs: http://localhost:8000/docs
