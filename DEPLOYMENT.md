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

Render is the best place to host this app because it supports the `render.yaml` Blueprint for zero-configuration deployment.

### 🚀 Zero-Config Deploy (Blueprints)
1.  **Push to GitHub**: Make sure `render.yaml` is in your repository.
2.  **Go to Render**: [dashboard.render.com](https://dashboard.render.com) -> New -> **Blueprint**.
3.  **Connect Repo**: Select your `sim800l-firebase` repo.
4.  **Apply**: Render will automatically detect the configuration from `render.yaml`.
5.  **Environment Variables**:
    - Render might ask for `GROQ_API_KEY`. Enter it.
6.  **Sit back**: Render handles the build and deploy.

### Manual Deploy (Web Service)
If you prefer manual setup without `render.yaml`:
1.  Create a **Web Service**.
2.  **Runtime**: Python 3.
3.  **Build Command**: `pip install -r requirements.txt`.
4.  **Start Command**: `gunicorn -c gunicorn.conf.py backend.app:app`.
5.  **Environment Variables**: Add `GROQ_API_KEY`.

*(Note: To get `g++` for C++ execution, use Option 3 below).*

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
