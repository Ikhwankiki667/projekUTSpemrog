# Gunakan image Python resmi
FROM python:3.10-slim

# Tentukan direktori kerja dalam container
WORKDIR /app

# Salin semua file proyek ke dalam container
COPY . .

# Install dependensi (kalau punya file requirements.txt)
RUN pip install --no-cache-dir -r requirements.txt

# Jalankan program utama (misalnya main.py)
CMD ["python", "main.py"]
