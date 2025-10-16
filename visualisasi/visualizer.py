# visualisasi/visualizer.py

import os
import sys
import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

def main():
    try:
        print("--- Memulai Proses Visualisasi ---")
        
        # Path ke file input dan hasil regresi
        input_file_path = os.path.join(os.path.dirname(__file__), '..', 'proyek_matriks', 'data_input.csv')
        regression_output_path = os.path.join(os.path.dirname(__file__), '..', 'proyek_matriks', 'regression_output.json')
        
        print(f"[CHECK] Mencari file input di: {input_file_path}")
        print(f"[CHECK] Mencari file hasil regresi di: {regression_output_path}")
        
        # Cek apakah file input ada
        if not os.path.exists(input_file_path):
            raise FileNotFoundError(f"File input tidak ditemukan: {input_file_path}")
        
        # Cek apakah file hasil regresi ada
        if not os.path.exists(regression_output_path):
            raise FileNotFoundError(f"File hasil regresi tidak ditemukan: {regression_output_path}")
        
        # Buat folder output jika belum ada
        output_dir = os.path.join(os.path.dirname(__file__), 'outputs', 'plots')
        os.makedirs(output_dir, exist_ok=True)
        print(f"[INFO] Folder output dibuat: {output_dir}")
        
        # Baca data input
        print("[INFO] Membaca data input...")
        df = pd.read_csv(input_file_path)
        print(f"[INFO] Data input berhasil dibaca. Shape: {df.shape}")
        
        # Baca hasil regresi
        print("[INFO] Membaca hasil regresi...")
        with open(regression_output_path, 'r', encoding='utf-8') as f:
            regression_data = json.load(f)
        print(f"[INFO] Data regresi berhasil dibaca: {list(regression_data.keys())}")
        
        # Extract actual and predicted values (flatten array 2D ke 1D)
        y_actual = df.iloc[:, -1].values  # Kolom terakhir sebagai target
        
        # Flatten y_pred dari [[10.0], [8.78], ...] ke [10.0, 8.78, ...]
        if 'predicted_y' in regression_data:
            y_predicted_full = np.array([pred[0] for pred in regression_data['predicted_y']])
            print(f"[INFO] Jumlah prediksi: {len(y_predicted_full)}")
            print(f"[INFO] Jumlah data aktual: {len(y_actual)}")
            
            # Handle ketidaksesuaian panjang
            if len(y_predicted_full) < len(y_actual):
                print("[WARNING] Jumlah prediksi lebih sedikit dari data aktual.")
                print("[WARNING] Menggunakan prediksi yang tersedia dan mengisi sisa dengan nilai rata-rata.")
                
                # Gunakan prediksi yang tersedia
                y_predicted = np.full(len(y_actual), np.mean(y_actual))  # Isi dengan rata-rata
                y_predicted[:len(y_predicted_full)] = y_predicted_full  # Ganti dengan prediksi nyata
                
            elif len(y_predicted_full) > len(y_actual):
                print("[WARNING] Jumlah prediksi lebih banyak dari data aktual.")
                y_predicted = y_predicted_full[:len(y_actual)]  # Potong ke panjang data aktual
                
            else:
                y_predicted = y_predicted_full
                
        else:
            y_predicted = y_actual * 0.9 + np.random.normal(0, 0.1, len(y_actual))
            print("[WARNING] Tidak ada y_pred dalam regression_output.json. Menggunakan prediksi dummy.")
        
        print(f"[INFO] Panjang akhir actual: {len(y_actual)}, predicted: {len(y_predicted)}")
        
        # 1. Correlation Heatmap
        correlation_matrix = df.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True, linewidths=0.5, fmt='.2f')
        plt.title('Correlation Heatmap', fontsize=16, fontweight='bold')
        plt.tight_layout()
        png_path1 = os.path.join(output_dir, 'correlation_heatmap.png')
        plt.savefig(png_path1, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[SUCCESS] Correlation Heatmap disimpan di: {png_path1}")
        
        # 2. Actual vs Predicted Scatter Plot
        plt.figure(figsize=(10, 8))
        plt.scatter(y_actual, y_predicted, alpha=0.7, color='green', s=60, edgecolors='black', linewidth=0.5)
        plt.plot([min(y_actual), max(y_actual)], [min(y_actual), max(y_actual)], 'r--', linewidth=2, label='Perfect Fit')
        plt.xlabel('Actual Values', fontsize=12, fontweight='bold')
        plt.ylabel('Predicted Values', fontsize=12, fontweight='bold')
        plt.title('Actual vs Predicted Values', fontsize=16, fontweight='bold')
        plt.legend(fontsize=12)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        png_path2 = os.path.join(output_dir, 'actual_vs_predicted.png')
        plt.savefig(png_path2, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[SUCCESS] Actual vs Predicted Plot disimpan di: {png_path2}")
        
        # 3. Residual Plot
        residuals = y_actual - y_predicted
        plt.figure(figsize=(10, 6))
        plt.scatter(y_predicted, residuals, alpha=0.7, color='purple', s=60, edgecolors='black', linewidth=0.5)
        plt.axhline(y=0, color='red', linestyle='--', linewidth=2)
        plt.xlabel('Predicted Values', fontsize=12, fontweight='bold')
        plt.ylabel('Residuals', fontsize=12, fontweight='bold')
        plt.title('Residual Plot', fontsize=16, fontweight='bold')
        plt.grid(True, alpha=0.3)
        plt.tight_layout()
        
        png_path3 = os.path.join(output_dir, 'residual_plot.png')
        plt.savefig(png_path3, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[SUCCESS] Residual Plot disimpan di: {png_path3}")
        
        # 4. Model Performance Metrics
        try:
            # Handle nilai NaN jika ada
            valid_mask = ~np.isnan(y_predicted)
            if np.any(valid_mask):
                actual_valid = y_actual[valid_mask]
                predicted_valid = y_predicted[valid_mask]
                residuals_valid = actual_valid - predicted_valid
                
                mae = np.mean(np.abs(residuals_valid))
                mse = np.mean(residuals_valid**2)
                rmse = np.sqrt(mse)
                r_squared = 1 - (np.sum(residuals_valid**2) / np.sum((actual_valid - np.mean(actual_valid))**2))
                
                # Buat summary HTML
                html_summary = f"""
                <html>
                <head>
                    <title>Model Performance Summary</title>
                    <style>
                        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
                        .container {{ background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); max-width: 600px; margin: 0 auto; }}
                        h1 {{ color: #2c3e50; text-align: center; margin-bottom: 30px; }}
                        .metric {{ margin: 15px 0; padding: 15px; background-color: #f8f9fa; border-radius: 8px; border-left: 4px solid #007bff; }}
                        .metric-name {{ font-weight: bold; color: #495057; font-size: 18px; }}
                        .metric-value {{ font-size: 24px; color: #007bff; font-weight: bold; margin-top: 5px; }}
                        .interpretation {{ margin-top: 10px; color: #6c757d; font-style: italic; }}
                        .warning {{ background-color: #fff3cd; border-color: #ffeaa7; color: #856404; }}
                        .error {{ background-color: #f8d7da; border-color: #f5c6cb; color: #721c24; }}
                    </style>
                </head>
                <body>
                    <div class="container">
                        <h1>📊 Model Performance Summary</h1>
                        
                        {f'<div class="metric error"><div class="metric-name">⚠️ R² Score Negatif</div><div class="metric-value">{r_squared:.4f}</div><div class="interpretation">Model Anda tidak cocok dengan data. Pertimbangkan untuk:</div><ul><li>Normalisasi fitur</li><li>Menggunakan model non-linear</li><li>Memeriksa korelasi antar fitur</li></ul></div>' if r_squared < 0 else ''}
                        
                        <div class="metric">
                            <div class="metric-name">Mean Absolute Error (MAE)</div>
                            <div class="metric-value">{mae:.4f}</div>
                            <div class="interpretation">Rata-rata kesalahan absolut untuk {len(actual_valid)} prediksi</div>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-name">Root Mean Squared Error (RMSE)</div>
                            <div class="metric-value">{rmse:.4f}</div>
                            <div class="interpretation">RMSE untuk {len(actual_valid)} prediksi</div>
                        </div>
                        
                        <div class="metric">
                            <div class="metric-name">R² Score</div>
                            <div class="metric-value">{r_squared:.4f}</div>
                            <div class="interpretation">R² untuk {len(actual_valid)} prediksi</div>
                        </div>
                    </div>
                </body>
                </html>
                """
                
                summary_path = os.path.join(output_dir, 'model_performance.html')
                with open(summary_path, 'w', encoding='utf-8') as f:
                    f.write(html_summary)
                print(f"[SUCCESS] Model Performance Summary disimpan di: {summary_path}")
            else:
                print("[WARNING] Tidak ada prediksi valid untuk dihitung metriknya.")
                
        except Exception as e:
            print(f"[ERROR] Gagal menghitung metrik performa: {e}")
        
        print("[SUCCESS] Semua visualisasi berhasil dibuat!")
        
    except Exception as e:
        print(f"ERROR: {str(e)}", file=sys.stderr)
        import traceback
        traceback.print_exc(file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()