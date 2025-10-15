import os
import sys
import traceback

# Menggunakan impor relatif untuk konsistensi
from .importers.csv_importer import CSVImporter
from .operations.regression import Regression
from .exporters.json_exporter import JSONExporter
from .matrix import Matrix

def main():
    """
    Fungsi utama untuk menjalankan alur kerja regresi.
    """
    try:
        # Tentukan path file relatif terhadap skrip ini
        base_dir = os.path.dirname(os.path.abspath(__file__))
        input_file = os.path.join(base_dir, 'data_input.csv')

        # === 1. Impor Data ===
        print("Data berhasil diimpor dari CSV.")
        importer = CSVImporter(input_file)
        matrix_data = importer.import_data()

        # === 2. Siapkan Matriks X (fitur) dan y (target) ===
        # Asumsikan kolom terakhir adalah y, sisanya adalah X
        X_data = [row[:-1] for row in matrix_data]
        y_data = [[row[-1]] for row in matrix_data]

        # Tambahkan kolom intercept (nilai 1) di awal X
        for row in X_data:
            row.insert(0, 1)

        X_matrix = Matrix(X_data)
        y_matrix = Matrix(y_data)
        print("Matriks X (fitur) dan y (target) berhasil disiapkan.")

        # === 3. Lakukan Regresi ===
        regression = Regression(X_matrix, y_matrix)
        beta_matrix = regression.fit()
        print("Perhitungan koefisien regresi (beta) berhasil.")

        # === 4. Ekspor Hasil (Koefisien Beta) ===
        # Tentukan path output
        output_dir = os.path.join(os.path.dirname(base_dir), 'visualisasi', 'outputs')
        
        # *** PERBAIKAN UTAMA: Buat direktori jika belum ada ***
        os.makedirs(output_dir, exist_ok=True)
        
        output_file = os.path.join(output_dir, 'regression_output.json')
        
        exporter = JSONExporter(output_file)
        exporter.export(beta_matrix, 'beta')
        print(f"Hasil regresi berhasil diekspor ke {output_file}")

    except Exception:
        # Menangkap error apa pun dan menampilkannya dengan detail
        print("\n--- TERJADI ERROR SAAT PROSES REGRESI ---")
        traceback.print_exc()
        sys.exit(1) # Keluar dengan status error

if __name__ == '__main__':
    main()

