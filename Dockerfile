
FROM python:3.12-slim

WORKDIR /app

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the Flask application
COPY application/ ./application/

# Configure Python application path
ENV PYTHONPATH=/app/application
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app/application

# Flask application port
EXPOSE 5000

# Start using Waitress
CMD ["waitress-serve", "--listen=0.0.0.0:5000", "run:app"]
