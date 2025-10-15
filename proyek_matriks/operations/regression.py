import json
import os

# --- PERUBAHAN KUNCI ---
# Gunakan impor relatif (..) untuk naik dua level dari 'operations' 
# ke direktori 'proyek_matriks' lalu masuk ke file matrix.py
from ..matrix import Matrix
from ..operations.invers import invers
from ..operations.transpose import transpose
from ..operations.multiplier import multiply_matrices

class Regression:
    def __init__(self, X, y):
        self.X = self._add_intercept(X)
        self.y = y
        self.beta = self._calculate_beta()

    def _add_intercept(self, X):
        """Menambahkan kolom intercept (nilai 1) di awal matriks X."""
        intercept = Matrix([[1] for _ in range(X.rows)])
        
        # Gabungkan kolom intercept dengan matriks X
        new_data = [intercept.get_row(i) + X.get_row(i) for i in range(X.rows)]
        return Matrix(new_data)

    def _calculate_beta(self):
        """Menghitung koefisien regresi (beta) menggunakan rumus OLS."""
        # Rumus: β = (X^T * X)^-1 * X^T * y
        Xt = transpose(self.X)
        XtX = multiply_matrices(Xt, self.X)
        XtX_inv = invers(XtX)
        Xty = multiply_matrices(Xt, self.y)
        beta = multiply_matrices(XtX_inv, Xty)
        return beta

    def predict(self, X_new):
        """Membuat prediksi y untuk data X baru."""
        X_new_intercept = self._add_intercept(X_new)
        return multiply_matrices(X_new_intercept, self.beta)

    def get_coefficients(self):
        """Mengembalikan koefisien beta."""
        return self.beta

    def save_results(self, output_dir="."):
        """Menyimpan hasil regresi (koefisien dan prediksi) ke file JSON."""
        # Membuat prediksi untuk data training asli
        y_pred = self.predict(self.X)

        result = {
            "coefficients": self.beta.get_data(),
            "predicted_values": y_pred.get_data(),
            "original_y": self.y.get_data(),
            "original_X_with_intercept": self.X.get_data()
        }
        
        # Pastikan direktori ada
        os.makedirs(output_dir, exist_ok=True)
        
        output_path = os.path.join(output_dir, "regression_output.json")
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=4)
        
        print(f"Hasil regresi disimpan di {output_path}")
