# Deployment Guide

## ⚠️ Important Note Before Deploying

This application has a **Code Execution Engine** that compiles and runs code.
- **Python / JS**: Will work on most platforms.
- **C++**: Requires `g++` (GCC), which is **NOT installed** on Vercel's standard environment.

For full features (including C++ support), use **Render, Railway, or a VPS**.

---

## Option 1: Vercel (Recommended for simple Python/JS testing)

Vercel is great for the frontend and simple Python execution, but C++ will fail.

1.  **Install Vercel CLI** (or use the Dashboard):
    ```bash
    npm i -g vercel
    ```
2.  **Deploy**:
    ```bash
    vercel
    ```
3.  **Environment Variables**:
    - Go to Vercel Dashboard -> Settings -> Environment Variables.
    - Add `GROQ_API_KEY`.

**Note**: The included `vercel.json` is configured to route API requests to `backend/app.py` and serve the `frontend/` folder.

---

## Option 2: Render (Recommended for FULL features)

Render can run a full Docker container or Python service, allowing C++ execution if configured.

1.  Create a `render.yaml` or "Web Service" in Render Dashboard.
2.  **Runtime**: Python 3.
3.  **Build Command**: `pip install -r requirements.txt`.
4.  **Start Command**: `gunicorn backend.app:app`.
5.  **Environment Variables**: Add `GROQ_API_KEY`.

*(Note: To get `g++` on Render's Python runtime, you may need to use a Dockerfile instead of the native Python runtime).*

---

## Option 3: Docker (Run Anywhere)

Create a `Dockerfile` to package everything (Python, Node, G++) together.

```dockerfile
FROM python:3.9-slim

# Install G++ and Node.js
RUN apt-get update && apt-get install -y g++ nodejs

WORKDIR /app
COPY . .
RUN pip install -r requirements.txt

CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:5000"]
```
