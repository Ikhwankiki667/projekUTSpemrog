# Gunakan Python resmi
FROM python:3.10-slim

# Atur direktori kerja di dalam container
WORKDIR /app

# Salin requirements dan instal
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Salin seluruh kode web_app
COPY . .

# Expose port Flask
EXPOSE 5000

# Jalankan Flask app
CMD ["python", "app.py"]
