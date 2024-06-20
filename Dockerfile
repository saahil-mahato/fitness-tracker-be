# Use the official Python image from the Docker Hub
FROM python:3.12-slim-bullseye

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Chrome
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    unzip \
    && wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
    && dpkg -i google-chrome-stable_current_amd64.deb || apt-get -fy install \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Add the Chrome WebDriver
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$(curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE)/chromedriver_linux64.zip \
    && unzip /tmp/chromedriver.zip -d /usr/local/bin/ \
    && rm /tmp/chromedriver.zip

# Install the dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set the environment variable to prevent Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE 1

# Set the environment variable to buffer stdout and stderr
ENV PYTHONUNBUFFERED 1

# Expose port 5000 for the Flask app
EXPOSE 5000

# Run the Flask app
CMD ["python", "app.py"]
