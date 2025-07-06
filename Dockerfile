FROM python:3.10-slim

# Install LibreOffice and fonts
RUN apt-get update && \
    apt-get install -y libreoffice libreoffice-writer fonts-dejavu && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy files
COPY . /app

# Install Python deps
RUN pip install --no-cache-dir -r requirements.txt

# Create temp dir for uploads
RUN mkdir -p /app/temp

# Start the app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "10000"]
