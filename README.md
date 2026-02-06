# ProCode AI - Python Edition

A production-ready, locally hosted Code Editor & AI Analyzer.
Combines a **Python/Flask/Groq** backend with a **Modern React/Vite** frontend.

## Features

- **Python-Only Engine**: Optimized execution with sub-millisecond overhead.
- **AI Integration**: Uses Groq (Llama 3) for real-time complexity analysis and code suggestions.
- **Modern UI**: Dark mode, glassmorphism, and fluid animations using React, Tailwind, and Framer Motion.
- **Secure Sandboxing**: Timeout-protected execution environment.

## Tech Stack

- **Backend**: Python (Flask) + Groq API
- **Frontend**: React (Vite) + Tailwind CSS + Framer Motion
- **Editor**: Monaco Editor (VS Code core)

## Setup & Run

### Prerequisites
- Python 3.8+
- Node.js & npm
- [Groq API Key](https://console.groq.com/)

### Installation

1.  **Clone & Install Backend**:
    ```bash
    git clone <repo-url>
    pip install -r requirements.txt
    ```

2.  **Environment Setup**:
    - Rename `.env.example` to `.env`
    - Add your API Key: `GROQ_API_KEY=gsk_...`

3.  **Install Frontend**:
    ```bash
    cd frontend
    npm install
    ```

### How to Run

You need **two** terminal windows:

**Terminal 1 (Backend)**:
```bash
python backend/app.py
```
*Runs on http://localhost:5000*

**Terminal 2 (Frontend)**:
```bash
cd frontend
npm run dev
```
*Runs on http://localhost:5173*

Open **http://localhost:5173** to use the application.
