import json
import os
import sys
import pandas as pd

# --- Menggunakan impor relatif ---
# Ini memastikan skrip bisa menemukan file lain di dalam paket 'visualisasi'
from .metrics import compute_metrics
from .plotter.plot_2d import plot_2d
from .plotter.plot_3d import plot_3d
from .plotter.plot_heatmap import plot_heatmap

def main():
    """
    Fungsi utama untuk menjalankan alur kerja visualisasi.
    """
    print("\n--- Memulai Proses Visualisasi ---")

    try:
        # Tentukan path file relatif terhadap skrip ini
        base_dir = os.path.dirname(os.path.abspath(__file__))
        output_dir = os.path.join(base_dir, 'outputs', 'plots')
        metrics_output_file = os.path.join(base_dir, 'outputs', 'metrics_summary.json')
        
        # Path ke file input dari proyek_matriks
        project_base_dir = os.path.dirname(os.path.dirname(base_dir))
        input_csv = os.path.join(project_base_dir, 'proyek_matriks', 'data_input.csv')
        regression_json = os.path.join(base_dir, 'outputs', 'regression_output.json')
        
        os.makedirs(output_dir, exist_ok=True)

        print("[CHECK] 1. Memuat data input dan hasil regresi...")
        # Memuat data asli untuk mendapatkan X dan y_true
        df_input = pd.read_csv(input_csv)
        X_df = df_input.iloc[:, :-1]
        y_true = df_input.iloc[:, -1].values.flatten()
        
        # Memuat koefisien beta dari hasil regresi
        with open(regression_json, 'r') as f:
            beta_data = json.load(f)
        beta = [item for sublist in beta_data['beta'] for item in sublist] # Flatten list
        print("    -> Berhasil.")

        print("[CHECK] 2. Menghitung nilai prediksi (y_pred)...")
        # Tambahkan kolom intercept (1) ke X
        X_with_intercept = X_df.copy()
        X_with_intercept.insert(0, 'intercept', 1)
        X_np = X_with_intercept.values
        
        # y_pred = X * beta
        y_pred = X_np.dot(beta)
        print("    -> Berhasil.")

        # Simpan data prediksi ke CSV untuk di-download
        df_pred = pd.DataFrame({'harga_aktual': y_true, 'harga_prediksi': y_pred})
        df_pred.to_csv(os.path.join(output_dir, 'data_prediksi.csv'), index=False)
        print("    -> File data_prediksi.csv berhasil dibuat.")

        print("[CHECK] 3. Menghitung metrik evaluasi (R^2, MSE, MAE)...")
        metrics = compute_metrics(y_true, y_pred)
        with open(metrics_output_file, 'w') as f:
            json.dump(metrics, f, indent=4)
        print("    -> Berhasil. Metrik disimpan di metrics_summary.json.")

        print("[CHECK] 4. Memulai pembuatan plot...")
        # Plot 2D: Perbandingan Aktual vs Prediksi (Selalu dibuat)
        print("    - Membuat plot 2D (Aktual vs Prediksi)...")
        plot_2d(y_true, y_pred, metrics, output_path=os.path.join(output_dir, "regression_plot_2d.html"))
        print("      -> Plot 2D berhasil dibuat.")

        # Plot 3D: Hanya jika ada tepat 2 fitur
        num_features = X_df.shape[1]
        if num_features == 2:
            print("    - Membuat plot 3D (Bidang Regresi)...")
            plot_3d(X_df.values, y_true, beta, output_path=os.path.join(output_dir, "regression_plot_3d.html"))
            print("      -> Plot 3D berhasil dibuat.")

        # Heatmap Korelasi
        print("    - Membuat heatmap korelasi...")
        plot_heatmap(df_input, output_path=os.path.join(output_dir, "regression_heatmap.png"))
        print("      -> Heatmap berhasil dibuat.")
        
    except FileNotFoundError as e:
        print(f"Error: File tidak ditemukan - {e}")
        sys.exit(1)
    except Exception as e:
        import traceback
        print(f"Terjadi error yang tidak terduga di visualizer: {e}")
        traceback.print_exc()
        sys.exit(1)

    print("--- Proses Visualisasi Selesai ---")

if __name__ == '__main__':
    main()

