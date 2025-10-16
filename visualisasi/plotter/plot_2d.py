# visualisasi/plotter/plot_2d.py

import matplotlib.pyplot as plt
import numpy as np

def create_2d_regression_plot(X_features, y_actual, regression_data, output_dir):
    """Buat plot regresi 2D"""
    if X_features.shape[1] == 1:  # Hanya 1 fitur
        X_1d = X_features.iloc[:, 0].values
        
        # Ambil koefisien dari regression_output.json
        intercept = 0
        coefficient = 1
        
        if 'intercept' in regression_data and 'coefficients' in regression_data:
            intercept = regression_data['intercept']
            coefficient = regression_data['coefficients'][0]
        
        # Buat plot regresi 2D
        plt.figure(figsize=(10, 6))
        plt.scatter(X_1d, y_actual, color='blue', label='Data Aktual', alpha=0.7)
        
        # Buat garis regresi
        X_line = np.linspace(min(X_1d), max(X_1d), 100)
        y_line = intercept + coefficient * X_line
        plt.plot(X_line, y_line, color='red', linewidth=2, label='Regresi')
        
        plt.xlabel('X')
        plt.ylabel('Y')
        plt.title('Regresi Linear (2D)')
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        
        png_path = os.path.join(output_dir, 'regression_2d.png')
        plt.savefig(png_path, dpi=300, bbox_inches='tight')
        plt.close()
        print(f"[SUCCESS] Regression 2D Plot disimpan di: {png_path}")