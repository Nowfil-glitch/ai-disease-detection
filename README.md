# AI Disease Detection Platform 🏥

A cutting-edge, AI-powered medical image analysis tool designed to assist healthcare professionals in preliminary diagnosis. This platform leverages deep learning to analyze medical images (X-rays, skin lesions, etc.) and provides instant risk assessments with visual explainability.

![Project Banner](product-pitch.pdf) <!-- You can replace this with a screenshot later -->

## 🚀 Key Features

*   **⚡ Instant AI Analysis**: Rapidly processes uploaded medical images using pre-trained deep learning models.
*   **🔍 Visual Explainability**: Generates Grad-CAM heatmaps to highlight the specific regions of the image that influenced the AI's decision.
*   **🌐 Multi-Language Support**: Automatically translates results into English, Hindi, Spanish, and French for broader accessibility.
*   **📊 Confidence Scoring**: Provides a detailed breakdown of risk levels and confidence percentages.
*   **🔒 Privacy-First Architecture**: Designed with local processing capabilities to ensure patient data security.

## 🛠️ Tech Stack

### Frontend
*   **Framework**: Next.js 14 (React)
*   **Language**: TypeScript
*   **Styling**: Tailwind CSS with Glassmorphism design
*   **Components**: Custom UI components with Framer Motion animations

### Backend
*   **Framework**: FastAPI (Python)
*   **AI/ML**: PyTorch, TensorFlow (compatible), PIL
*   **Image Processing**: OpenCV, NumPy

## 🏃‍♂️ Quick Start

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

## ⚠️ Disclaimer
**For Educational Purposes Only.** This tool is intended for demonstration and research. It is **not** a certified medical device and should not be used for actual clinical diagnosis or treatment decisions. Always consult a qualified healthcare professional.
