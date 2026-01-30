FROM python:3.10-slim

# Install system dependencies for FAISS and other libraries
RUN apt-get update && apt-get install -y \
    libgomp1 \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8080

# Create and change to the app directory.
WORKDIR /app

# Copy application dependency file to the container image.
COPY requirements.txt ./

# Install dependencies.
RUN pip install --no-cache-dir -r requirements.txt

# Copy local code to the container image.
COPY . .

# Run the web service on container startup.
CMD exec uvicorn server:app --host 0.0.0.0 --port $PORT
