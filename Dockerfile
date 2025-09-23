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
