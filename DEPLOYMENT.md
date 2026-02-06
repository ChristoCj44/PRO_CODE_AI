# Deployment Guide

## ⚠️ Important Note Before Deploying

This application has a **Code Execution Engine** that compiles and runs code.
- **Python / JS**: Will work on most platforms.
- **C++**: Requires `g++` (GCC), which is **NOT installed** on Vercel's standard environment.

For full features (including C++ support), use **Render, Railway, or a VPS**.

---

## Option 1: Vercel (Free & Easy)

**Best for:** Free hosting, simple deployment, separate frontend/backend.
**Limitations:** No C++ support (Python automation only).

### Steps
1.  **Push to GitHub**:
    Ensure your code is committed and pushed to your GitHub repository.
    ```bash
    git add .
    git commit -m "Ready for deployment"
    git push origin main
    ```

2.  **Create Vercel Project**:
    - Go to [vercel.com/new](https://vercel.com/new).
    - Import your GitHub repository (`sim800l-firebase`).

3.  **Configure Project**:
    - **Framework Preset**: Select "Other" (or leave as Default).
    - **Root Directory**: Leave as `./`.
    - **Build & Output Settings**: Leave default.
    - **Environment Variables**:
        - Key: `GROQ_API_KEY`
        - Value: `your_api_key_here`

4.  **Deploy**:
    - Click **Deploy**.
    - Vercel will detect `vercel.json` and set up the routing:
        - `https://your-app.vercel.app/` -> Serves `frontend/index.html`
        - `https://your-app.vercel.app/execute` -> Hits Flask Backend

### Troubleshooting Vercel
- If you see `404` on the backend, check the "Functions" tab in Vercel to see if the Python build failed.
- Ensure `requirements.txt` is in the root directory.

---

## Option 2: Render (Recommended for FULL features)

Render can run a full Docker container or Python service, allowing C++ execution if configured.

1.  Create a `render.yaml` or "Web Service" in Render Dashboard.
2.  **Runtime**: Python 3.
3.  **Build Command**: `pip install -r requirements.txt`.
4.  **Start Command**: `gunicorn -c gunicorn.conf.py backend.app:app`.
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

CMD ["gunicorn", "-c", "gunicorn.conf.py", "backend.app:app"]
```
