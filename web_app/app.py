from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import subprocess
import sys
import shutil
import csv
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = "matrix-secret-key"

# === Konfigurasi Path yang Kuat ===
# BASE_DIR menunjuk ke folder web_app (lokasi file app.py ini berada)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Lokasi project utama (satu level di atas web_app)
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Lokasi skrip backend sebagai modul
MATRIX_MODULE = "proyek_matriks.main"
VISUALIZER_MODULE = "visualisasi.visualizer"

# Lokasi sumber plot (tempat file dibuat oleh backend)
SRC_VIS_DIR = os.path.join(PROJECT_ROOT, "visualisasi", "outputs", "plots")
# Lokasi tujuan plot (agar bisa diakses oleh browser)
DEST_VIS_DIR = os.path.join(BASE_DIR, "static", "plots")

# Pastikan direktori static/plots ada
os.makedirs(DEST_VIS_DIR, exist_ok=True)

def validate_csv_file(filepath):
    """Validasi file CSV dasar"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            sniffer = csv.Sniffer()
            sample = f.read(1024)
            f.seek(0)
            if not sniffer.has_header(sample):
                return False, "File CSV harus memiliki header di baris pertama."
            
            # Cek minimal 2 kolom (fitur + target)
            reader = csv.reader(f)
            headers = next(reader)
            if len(headers) < 2:
                return False, "File CSV harus memiliki minimal 2 kolom (fitur dan target)."
                
        return True, "Valid"
    except Exception as e:
        return False, f"Error saat memvalidasi file CSV: {str(e)}"

@app.route('/')
def index():
    """Menampilkan halaman utama."""
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    """Menangani upload file dan menjalankan seluruh pipeline."""
    if 'file' not in request.files or request.files['file'].filename == '':
        flash('❌ Tidak ada file yang dipilih. Silakan pilih file CSV.', 'error')
        return redirect(request.url)

    file = request.files['file']
    
    # Simpan file upload ke lokasi yang benar untuk diproses
    upload_path = os.path.join(PROJECT_ROOT, "proyek_matriks", "data_input.csv")
    
    # Pastikan direktori tujuan ada
    os.makedirs(os.path.dirname(upload_path), exist_ok=True)
    
    file.save(upload_path)
    flash('✅ File berhasil diupload.', 'success')

    try:
        python_exec = sys.executable

        # --- LANGKAH 1: Jalankan Perhitungan Regresi ---
        flash('⚙️ Memulai perhitungan regresi...', 'info')
        result_matrix = subprocess.run(
            [python_exec, "-m", MATRIX_MODULE], 
            capture_output=True, text=True, check=True, cwd=PROJECT_ROOT
        )
        if result_matrix.stdout:
            flash(f"INFO (Regresi): {result_matrix.stdout.strip()}", 'info')
        flash('📘 Perhitungan regresi selesai.', 'success')
            
        # --- LANGKAH 2: Jalankan Visualisasi ---
        flash('📊 Memulai pembuatan visualisasi...', 'info')
        result_vis = subprocess.run(
            [python_exec, "-m", VISUALIZER_MODULE], 
            capture_output=True, text=True, check=True, cwd=PROJECT_ROOT
        )
        
        # Tampilkan output dan error untuk debugging
        if result_vis.stdout:
            flash(f"INFO (Visualisasi): {result_vis.stdout.strip()}", 'info')
        if result_vis.stderr:
            flash(f"ERROR (Visualisasi): {result_vis.stderr.strip()}", 'error')
        
        # Tambahkan pesan debug
        flash(f"🟢 Status eksekusi visualisasi: {result_vis.returncode}", 'info')
            
        flash('📈 Visualisasi berhasil dibuat.', 'success')

        # --- LANGKAH 3: Salin Hasil Plot ke Folder Web ---
        if os.path.exists(DEST_VIS_DIR):
            shutil.rmtree(DEST_VIS_DIR)
        
        if os.path.exists(SRC_VIS_DIR):
            shutil.copytree(SRC_VIS_DIR, DEST_VIS_DIR)
            num_files = len([f for f in os.listdir(DEST_VIS_DIR) if f.endswith(('.html', '.png'))])
            flash(f'📂 Berhasil menyalin {num_files} file visualisasi.', 'info')
        else:
            flash('⚠️ Folder sumber visualisasi tidak ditemukan.', 'warning')

    except subprocess.CalledProcessError as e:
        error_message = e.stderr.strip() if e.stderr else "Skrip gagal tanpa pesan error."
        flash('⚠️ Terjadi kegagalan saat menjalankan skrip!', 'error')
        flash(f'PESAN ERROR: {error_message}', 'error')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'⚠️ Error tidak terduga: {str(e)}', 'error')
        return redirect(url_for('index'))
    
    return redirect(url_for('result'))

@app.route('/result')
def result():
    """Menampilkan halaman hasil dengan semua plot yang ditemukan."""
    plots = []
    if os.path.exists(DEST_VIS_DIR):
        for file in sorted(os.listdir(DEST_VIS_DIR)):
            if file.endswith((".html", ".png")):
                plots.append(file)
    
    return render_template('result.html', plots=plots)

@app.route('/download')
def download():
    """Menangani permintaan unduh file prediksi."""
    pred_path = os.path.join(DEST_VIS_DIR, 'data_prediksi.csv')
    if os.path.exists(pred_path):
        return send_file(pred_path, as_attachment=True, download_name='data_prediksi.csv')
    flash("⚠️ File data prediksi tidak ditemukan.", "error")
    return redirect(url_for('result'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)