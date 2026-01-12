# AI Disease Detection Platform

A full-stack AI-powered medical image analysis platform.

## Quick Start

### Backend (Terminal 1)
```bash
cd ai-backend
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
python create_demo_models.py
python -m app.main
```

### Frontend (Terminal 2)
```bash
cd ai-disease-ui
npm install
npm run dev
```

## URLs
- Frontend: http://localhost:3000
- Backend: http://localhost:8000
- API Docs: http://localhost:8000/docs

## Features
- AI medical image analysis (X-ray, skin, bone)
- Grad-CAM heatmap visualization
- Multi-language translations
- Risk level assessment

⚠️ **Educational use only. Not for medical diagnosis.**
