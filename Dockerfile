# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies (if any are needed for numpy/pandas, though slim usually has enough)
# RUN apt-get update && apt-get install -y gcc

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port the app runs on (Cloud Run defaults to 8080)
ENV PORT=8080
EXPOSE 8080

# Run server.py when the container launches
CMD ["python", "server.py"]
