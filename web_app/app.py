from flask import Flask, render_template, request, send_file, redirect, url_for, flash
import os
import subprocess
import sys
import shutil

app = Flask(__name__)
app.secret_key = "matrix-secret-key"

# === Path absolut relatif terhadap proyek utama ===
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VIS_SCRIPT_MODULE = "visualisasi.visualizer"

# Folder hasil visualisasi
SRC_VIS_DIR = os.path.join(BASE_DIR, "visualisasi", "outputs", "plots")
VIS_DIR = os.path.join(BASE_DIR, "web_app", "static", "plots")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('❌ Tidak ada file yang diupload')
        return redirect(url_for('index'))

    file = request.files['file']
    if file.filename == '':
        flash('❌ Tidak ada file yang dipilih')
        return redirect(url_for('index'))

    # Simpan file upload ke lokasi yang akan dibaca oleh proyek_matriks
    matrix_dir = os.path.join(BASE_DIR, "proyek_matriks")
    save_path = os.path.join(matrix_dir, 'data_input.csv')
    file.save(save_path)
    flash('✅ File berhasil diupload.')

    try:
        python_exec = sys.executable

        # --- LANGKAH 1: JALANKAN PERHITUNGAN REGRESI DENGAN ERROR CAPTURING ---
        flash('⚙️ Memulai perhitungan regresi...')
        proc_matriks = subprocess.run(
            [python_exec, "-m", "proyek_matriks.main"],
            cwd=BASE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        # Jika ada output, tampilkan untuk info
        if proc_matriks.stdout:
            # Tampilkan setiap baris output untuk kejelasan
            for line in proc_matriks.stdout.strip().split('\n'):
                flash(f'INFO (Regresi): {line}')

        flash('📘 Perhitungan regresi selesai.')

        # --- LANGKAH 2: JALANKAN VISUALISASI ---
        flash('📊 Memulai pembuatan visualisasi...')
        proc_vis = subprocess.run(
            [python_exec, "-m", VIS_SCRIPT_MODULE],
            cwd=BASE_DIR,
            check=True,
            capture_output=True,
            text=True
        )
        if proc_vis.stdout:
            for line in proc_vis.stdout.strip().split('\n'):
                flash(f'INFO (Visualisasi): {line}')
        flash('📈 Visualisasi berhasil dibuat.')

        # --- LANGKAH 3: PINDAHKAN HASIL PLOT ---
        os.makedirs(VIS_DIR, exist_ok=True)
        if os.path.exists(SRC_VIS_DIR):
            for f in os.listdir(SRC_VIS_DIR):
                shutil.copy2(os.path.join(SRC_VIS_DIR, f), os.path.join(VIS_DIR, f))

    except subprocess.CalledProcessError as e:
        # INI BAGIAN PALING PENTING: MENANGKAP DAN MENAMPILKAN ERROR
        flash('⚠️ Terjadi kegagalan saat menjalankan skrip!')
        # Tampilkan pesan error dari terminal (stderr) baris per baris
        for line in e.stderr.strip().split('\n'):
            flash(f'PESAN ERROR: {line}')
        return redirect(url_for('index'))
    except Exception as e:
        flash(f'⚠️ Terjadi kesalahan umum yang tidak terduga: {e}')
        return redirect(url_for('index'))

    return redirect(url_for('result'))

@app.route('/result')
def result():
    """Tampilkan hasil visualisasi dan tombol download CSV"""
    pred_path = os.path.join(VIS_DIR, 'data_prediksi.csv')

    plots = []
    if os.path.exists(VIS_DIR):
        for file in os.listdir(VIS_DIR):
            if file.endswith((".html", ".png")):
                plots.append(file)

    return render_template('result.html', plots=plots, pred_available=os.path.exists(pred_path))

@app.route('/download')
def download():
    """Download file hasil prediksi"""
    pred_path = os.path.join(VIS_DIR, 'data_prediksi.csv')
    if os.path.exists(pred_path):
        return send_file(pred_path, as_attachment=True)
    else:
        flash("⚠️ File data_prediksi.csv belum tersedia.")
        return redirect(url_for('result'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)

