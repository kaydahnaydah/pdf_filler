# Use official Python image from Docker Hub
FROM python:3.9-slim

# Set working directory inside the container
WORKDIR /app

# Copy and install requirements
COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

# Copy all files from current directory to /app in the container
COPY . .

# Expose port 5001 for Flask app
EXPOSE 5001

# Command to run the application
CMD ["python", "run.py"]