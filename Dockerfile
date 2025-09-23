# Gunakan image Python sebagai base
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install dependency sistem (buat OpenCV, Ultralytics, dsb)
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt ke container
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy semua file project
COPY . .

# Expose port Railway (akan dibaca dari ENV $PORT)
EXPOSE 8000

# Jalankan app dengan Gunicorn
CMD ["gunicorn", "-b", "0.0.0.0:8000", "app:app"]
# Atau jika menggunakan Uvicorn
# CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]