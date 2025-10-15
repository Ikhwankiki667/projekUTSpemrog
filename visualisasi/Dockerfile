# Gunakan Python resmi
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Salin requirements dan instal dependensi
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode ke dalam container
COPY . .

# Jalankan visualizer.py saat container dijalankan
CMD ["python", "visualizer.py"]
