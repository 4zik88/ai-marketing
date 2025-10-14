# Dockerfile for containerized deployment
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt requirements_web.txt ./
RUN pip install --no-cache-dir -r requirements.txt -r requirements_web.txt

# Copy application code
COPY . .

# Create output directory
RUN mkdir -p output

# Expose port
EXPOSE 5000

# Set environment variables
ENV FLASK_APP=web_app.py
ENV FLASK_ENV=production

# Run the application
CMD ["gunicorn", "wsgi:app", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "300"]
