# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy everything into container
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run main file
CMD ["python", "main.py"]