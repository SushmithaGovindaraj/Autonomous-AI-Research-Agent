# 🚀 Deployment Guide

This agent is built as a modern web application with a **FastAPI backend** and a **custom HTML/JS frontend**. It is ready to be deployed on any cloud platform that supports Python.

We recommend **Render** or **Railway** for the easiest, free deployment.

---

## Option 1: Deploy on Render (Recommended)

1.  **Push your code to GitHub** (if you haven't already).
2.  Sign up at [render.com](https://render.com/).
3.  Click **"New +"** -> **"Web Service"**.
4.  Connect your GitHub repository.
5.  **Configure the settings**:
    *   **Name**: `autonomous-research-agent` (or similar)
    *   **Runtime**: `Python 3`
    *   **Build Command**: `pip install -r requirements.txt`
    *   **Start Command**: `python server.py` (or let it use the `Procfile`)
6.  **Environment Variables** (Scroll down to "Advanced"):
    *   Click **"Add Environment Variable"**
    *   Key: `ANTHROPIC_API_KEY`
    *   Value: `your-actual-api-key-starting-with-sk-ant...`
7.  Click **"Create Web Service"**.

Render will build and deploy your app. Once finished, it will give you a URL (e.g., `https://my-agent.onrender.com`) where your live website is running!

---

## Option 2: Deploy on Railway

1.  **Push your code to GitHub**.
2.  Sign up at [railway.app](https://railway.app/).
3.  Click **"New Project"** -> **"Deploy from GitHub repo"**.
4.  Select your repository.
5.  Railway will automatically detect the `Procfile` and `requirements.txt`.
6.  **Add Variables**:
    *   Go to the **"Variables"** tab.
    *   Add `ANTHROPIC_API_KEY` with your API key.
7.  Railway will automatically redeploy.

---

## Option 3: Deploy on Google Cloud Platform (Cloud Run)

This is a professional, scalable option perfect for this application.

### Prerequisites
*   A Google Cloud Project
*   [Google Cloud SDK](https://cloud.google.com/sdk/docs/install) installed (or use Cloud Shell)

### Steps
1.  **Initialize Google Cloud**:
    ```bash
    gcloud init
    ```

2.  **Deploy to Cloud Run**:
    Run this single command from your project directory:
    ```bash
    gcloud run deploy autonomous-research-agent --source .
    ```

3.  **Configuration Prompts**:
    *   **Source code location**: Default (current directory)
    *   **Region**: Select one near you (e.g., `us-central1`)
    *   **Allow unauthenticated invocations**: **Yes** (y) (so the public can access your website)

4.  **Set Environment Variables**:
    After deployment, go to the [Cloud Run Console](https://console.cloud.google.com/run):
    *   Click on your service (`autonomous-research-agent`)
    *   Click **"Edit & Deploy New Revision"**
    *   Go to the **"Variables & Secrets"** tab
    *   Add Variable: `ANTHROPIC_API_KEY` with your value
    *   Click **"Deploy"**

Your agent is now live on Google Cloud with a production-grade URL!
