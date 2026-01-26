#!/bin/bash

# Configuration
PROJECT_ID="hip-service-485515-t9"
SERVICE_NAME="autonomous-research-agent"
REGION="us-central1"

echo "🚀 Starting deployment to Google Cloud Platform..."
echo "Project ID: $PROJECT_ID"
echo "Service Name: $SERVICE_NAME"

# 1. Set the active project
echo "📍 Setting gcloud project to $PROJECT_ID..."
gcloud config set project $PROJECT_ID

# 2. Enable necessary APIs
echo "⚙️ Enabling Cloud Run and Cloud Build APIs..."
gcloud services enable run.googleapis.com cloudbuild.googleapis.com

# 3. Deploy to Cloud Run
# This will automatically package your app and host it
echo "📦 Deploying source code to Cloud Run..."
gcloud run deploy $SERVICE_NAME \
  --source . \
  --region $REGION \
  --allow-unauthenticated \
  --quiet

echo "✅ Deployment finished!"
echo "------------------------------------------------"
echo "🌐 Your website will be available at the URL shown above."
echo ""
echo "⚠️ IMPORTANT: Don't forget to set your ANTHROPIC_API_KEY in the Google Cloud Console"
echo "under Cloud Run -> $SERVICE_NAME -> Edit & Deploy New Revision -> Variables."
echo "------------------------------------------------"
