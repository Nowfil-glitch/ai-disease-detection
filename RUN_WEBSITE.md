# 🚀 How to Run the AI Disease Detection Website

## Prerequisites

Before you begin, make sure you have:
- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **Node.js 18+** - [Download](https://nodejs.org/)

## Quick Start

### Option 1: Using Start Scripts

**Windows:**
```bash
start-all.bat
```

**Mac/Linux:**
```bash
chmod +x start-all.sh
./start-all.sh
```

### Option 2: Manual Setup

#### Step 1: Setup Backend

Open a terminal and run:

```bash
cd ai-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Create demo AI models (first time only)
python create_demo_models.py

# Start the backend server
python -m app.main
```

The backend will start at: **http://localhost:8000**

#### Step 2: Setup Frontend

Open a NEW terminal and run:

```bash
cd ai-disease-ui

# Install dependencies
npm install

# Start the development server
npm run dev
```

The frontend will start at: **http://localhost:3000**

#### Step 3: Open the Website

Open your browser and go to: **http://localhost:3000**

## Using the Application

1. **Upload Image**: Drag and drop or click to upload a medical image
2. **Analyze**: Click the "Analyze Image" button
3. **View Results**: See the AI diagnosis, confidence score, and heatmap
4. **Change Language**: Use the language selector to view translations

## Stopping the Servers

Press `Ctrl+C` in each terminal window to stop the servers.

Or use the stop scripts:
- Windows: `stop-all.bat`
- Mac/Linux: `./stop-all.sh`

## URLs

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Backend API | http://localhost:8000 |
| API Documentation | http://localhost:8000/docs |
| Health Check | http://localhost:8000/health |

## Troubleshooting

### Backend Issues

**"Module not found" error:**
```bash
pip install -r requirements.txt
```

**"Models not found" error:**
```bash
python create_demo_models.py
```

**Port 8000 already in use:**
```bash
# Windows
netstat -ano | findstr :8000
taskkill /F /PID <PID>

# Mac/Linux
lsof -i :8000
kill -9 <PID>
```

### Frontend Issues

**"npm not found":**
Install Node.js from https://nodejs.org/

**Dependencies error:**
```bash
rm -rf node_modules
npm install
```

**Port 3000 already in use:**
```bash
# Change port in package.json or kill the process
npx kill-port 3000
```

### Connection Issues

**CORS Error:**
Make sure the backend `.env` file includes:
```
ALLOWED_ORIGINS=http://localhost:3000
```

**"Failed to fetch" error:**
Make sure the backend is running at http://localhost:8000

## Development Tips

### Backend Hot Reload
The backend automatically reloads when you change files (DEBUG=True).

### Frontend Hot Reload
Next.js automatically reloads the browser when you save changes.

### View API Documentation
Visit http://localhost:8000/docs for interactive API testing.

## File Locations

- Backend code: `ai-backend/app/`
- Frontend code: `ai-disease-ui/app/` and `ai-disease-ui/components/`
- AI Models: `ai-backend/models/`
- Heatmaps: `ai-backend/static/heatmaps/`

---

⚠️ **Note:** This is for educational purposes only. Not for actual medical diagnosis.
