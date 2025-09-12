# Use official Python image
FROM python:3.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set working directory
WORKDIR /app

# Copy files into the container
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install flask flask_sqlalchemy flask_bcrypt email-validator

# Expose port (adjust if needed)
EXPOSE 5000

# Run the application
CMD ["python", "app.py"]
