<<<<<<< HEAD
# Use a base image with a specific version of Python
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose the port your application will run on
EXPOSE 5000

# Define the command to run your application when the container starts
CMD ["python", "app.py"]
=======
# Use a base Python image
FROM python:3.13-slim

# Install all necessary system dependencies here
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libgthread-2.0-0 \
    libsm6 \
    libxrender1 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements and install Python dependencies
# Now with a cache ID
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip,id=pip-cache \
    pip install --no-cache-dir -r requirements.txt

# Copy your application code
COPY . .

# Set the startup command
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app:app"]
>>>>>>> e0f89a41e027ec4dc4c3809cf537d4c81ab0cb92
