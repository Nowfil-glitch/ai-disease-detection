# 🌐 AI Disease Detection Platform - Deployment Guide

This guide provides step-by-step instructions to deploy your platform to production using **Render** for the backend and **Vercel** for the frontend.

## 🏗️ Architecture Overview
- **Backend**: FastAPI (Python 3.12) running in a Docker container on Render.
- **Frontend**: Next.js (React) deployed on Vercel.
- **AI Models**: Automatically initialized on the backend via `entrypoint.sh`.

---

## 1. 🚀 Backend Deployment (Render)

Render will use the `Dockerfile` in the `ai-backend` directory.

### Steps:
1. **Create a New Web Service**:
   - Log in to [Render](https://render.com).
   - Click **New +** > **Web Service**.
   - Connect your GitHub repository.
2. **Configure Service**:
   - **Root Directory**: `ai-backend`
   - **Runtime**: `Docker`
3. **Environment Variables**:
   Click **Advanced** and add the following:
   | Key | Value | Description |
   |-----|-------|-------------|
   | `BASE_URL` | `https://your-backend.onrender.com` | Your Render URL (after creation) |
   | `ALLOWED_ORIGINS` | `https://your-frontend.vercel.app` | Your Vercel URL |
   | `DEBUG` | `False` | Disable debug mode in production |

> [!TIP]
> Render provides a dynamic `$PORT`. The backend is already optimized to detect and use this automatically.

---

## 2. 🎨 Frontend Deployment (Vercel)

Vercel will build and host the Next.js application.

### Steps:
1. **Create a New Project**:
   - Log in to [Vercel](https://vercel.com).
   - Click **Add New** > **Project**.
   - Import your GitHub repository.
2. **Configure Project**:
   - **Root Directory**: `ai-disease-ui`
   - **Framework Preset**: `Next.js`
3. **Environment Variables**:
   Add the following variable:
   | Key | Value | Description |
   |-----|-------|-------------|
   | `NEXT_PUBLIC_API_URL` | `https://your-backend.onrender.com` | The URL of your Render backend |

---

## 🛠️ Troubleshooting & Verification

### 1. Check Backend Health
Once deployed, visit: `https://your-backend.onrender.com/health`
It should return `{"status": "healthy"}`.

### 2. AI Model Loading
The first build on Render might take several minutes as it downloads the pre-trained AI weights (approx. 500MB+). This is expected behavior managed by our `entrypoint.sh`.

### 3. CORS Issues
If the frontend fails to fetch results, ensure that `ALLOWED_ORIGINS` in Render exactly matches your Vercel URL (including `https://` and excluding trailing slashes).

---

## 🔒 Security Notes
- Ensure `SECRET_KEY` in backend environment variables is set to a long, random string.
- The system is for **educational purposes only** and should display the medical disclaimer prominently.
