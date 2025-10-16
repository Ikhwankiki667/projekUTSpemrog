# proyek_matriks/main.py

import os
import traceback
from .importers.csv_importer import CSVImporter
from .matrix import Matrix
from .operations.regression import Regression
from .exporters.json_exporter import JSONExporter

def main():
    """
    Alur kerja utama untuk regresi dataset rumah.
    """
    try:
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(base_dir, 'data_input.csv')
        output_dir = os.path.join(base_dir, '..', 'visualisasi', 'outputs')
        output_file = os.path.join(output_dir, 'regression_output.json')

        print(f"INFO: Memproses dataset rumah...")
        
        os.makedirs(output_dir, exist_ok=True)
        
        # Impor data
        importer = CSVImporter(input_file)
        data = importer.import_data()
        if data is None:
            raise ValueError("Gagal mengimpor data.")
        
        print(f"INFO: Dataset memiliki {len(data)} rumah")
        
        # Buat matriks X dengan bias term [1, luas_tanah, jumlah_kamar]
        X_data = [[1, row[0], row[1]] for row in data]  # [1, luas_tanah, jumlah_kamar]
        y_data = [[row[2]] for row in data]             # [harga_rumah]
        
        X = Matrix(X_data)
        y = Matrix(y_data)

        # Jalankan regresi
        print("INFO: Menjalankan regresi linear...")
        regression = Regression(X, y)
        regression.run()
        print("INFO: Regresi selesai.")
        
        # 🔴 PINDAHKAN KODE DEBUGGING KE SINI (di dalam blok try)
        print("INFO: Validasi hasil regresi...")
        beta_data = regression.beta.get_data()
        y_pred_data = regression.y_pred.get_data()

        print(f"INFO: Koefisien beta: {beta_data}")
        print(f"INFO: Beberapa prediksi pertama: {y_pred_data[:5]}")
        print(f"INFO: Beberapa nilai aktual pertama: {[[row[2]] for row in data[:5]]}")

        # Validasi range prediksi
        pred_values = [pred[0] for pred in y_pred_data]
        actual_values = [row[2] for row in data]
        print(f"INFO: Range prediksi: {min(pred_values):.2f} - {max(pred_values):.2f}")
        print(f"INFO: Range aktual: {min(actual_values):.2f} - {max(actual_values):.2f}")
        
        # Validasi hasil
        if len(regression.y_pred.get_data()) != len(data):
            raise ValueError(f"Ketidaksesuaian prediksi: {len(regression.y_pred.get_data())} vs {len(data)}")
        
        # Ekspor hasil
        exporter = JSONExporter(output_file)
        exporter.export(regression)
        print(f"INFO: Hasil disimpan ke {output_file}")

    except Exception as e:
        print(f"ERROR: {e}")
        traceback.print_exc()
        exit(1)

if __name__ == '__main__':
    main()