# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    gunicorn \
    wget \
    unzip \
    gnupg \
    dnsutils \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Set the environment variable to buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "wsgi:app"]
