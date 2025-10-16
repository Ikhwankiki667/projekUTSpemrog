# operations/regression.py (versi diperbaiki)

import math
from ..matrix import Matrix
from ..operations.transpose import transpose
from ..operations.multiplier import multiply_matrices
from ..operations.invers import invers

class Regression:
    def __init__(self, X, y):
        self.X = X
        self.y = y
        self.beta = None
        self.y_pred = None
        self.feature_means = None
        self.feature_stds = None
        self.y_mean = None
        self.y_std = None

    def _normalize_features_and_target(self):
        """Normalisasi fitur DAN target untuk stabilitas numerik."""
        data = self.X.get_data()
        y_data = self.y.get_data()
        n_rows = len(data)
        n_cols = len(data[0])
        
        if n_cols <= 1:
            return self.X, self.y, None, None, None, None
        
        # Normalisasi target y
        y_values = [row[0] for row in y_data]
        self.y_mean = sum(y_values) / n_rows
        y_variance = sum((y - self.y_mean) ** 2 for y in y_values) / n_rows
        self.y_std = math.sqrt(y_variance) if y_variance > 0 else 1.0
        y_normalized = [[(y - self.y_mean) / self.y_std] for y in y_values]
        y_norm_matrix = Matrix(y_normalized)
        
        # Normalisasi fitur (kecuali kolom bias pertama)
        features = []
        for row in data:
            features.append(row[1:])
        
        n_features = len(features[0])
        means = []
        stds = []
        
        for j in range(n_features):
            col_values = [features[i][j] for i in range(n_rows)]
            mean_val = sum(col_values) / n_rows
            variance = sum((x - mean_val) ** 2 for x in col_values) / n_rows
            std_val = math.sqrt(variance) if variance > 0 else 1.0
            means.append(mean_val)
            stds.append(std_val)
        
        normalized_data = []
        for i in range(n_rows):
            row = [data[i][0]]  # Keep bias term as 1
            for j in range(n_features):
                normalized_val = (features[i][j] - means[j]) / (stds[j] if stds[j] != 0 else 1.0)
                row.append(normalized_val)
            normalized_data.append(row)
        
        return Matrix(normalized_data), y_norm_matrix, means, stds, self.y_mean, self.y_std

    def _denormalize_predictions(self, y_pred_normalized):
        """Mengembalikan prediksi ke skala asli."""
        if self.y_mean is not None and self.y_std is not None:
            return [[pred[0] * self.y_std + self.y_mean] for pred in y_pred_normalized]
        return y_pred_normalized

    def run(self):
        """Menjalankan regresi linear dengan normalisasi penuh."""
        X_norm, y_norm, self.feature_means, self.feature_stds, self.y_mean, self.y_std = self._normalize_features_and_target()
        
        # Hitung beta dengan data yang dinormalisasi
        Xt = transpose(X_norm)
        XtX = multiply_matrices(Xt, X_norm)
        XtX_inv = invers(XtX)
        XtY = multiply_matrices(Xt, y_norm)
        self.beta = multiply_matrices(XtX_inv, XtY)
        
        # Prediksi dalam skala normalisasi
        y_pred_norm = multiply_matrices(X_norm, self.beta)
        
        # Kembalikan ke skala asli
        self.y_pred = Matrix(self._denormalize_predictions(y_pred_norm.get_data()))

    def get_results(self):
        return {
            "beta_coefficients": self.beta.get_data(),
            "predicted_y": self.y_pred.get_data()
        }