from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
import numpy as np

def compute_metrics(y_true, y_pred):
    """
    Menghitung metrik regresi: R², RMSE, dan MAE
    Menyesuaikan panjang y_true dan y_pred jika tidak sama.
    """
    y_true = np.array(y_true).flatten()
    y_pred = np.array(y_pred).flatten()

    # Samakan panjang data untuk menghindari error
    min_len = min(len(y_true), len(y_pred))
    y_true = y_true[:min_len]
    y_pred = y_pred[:min_len]

    # Hitung metrik
    r2 = r2_score(y_true, y_pred)
    rmse = np.sqrt(mean_squared_error(y_true, y_pred))
    mae = mean_absolute_error(y_true, y_pred)

    return {
        "R2_Score": float(r2),
        "RMSE": float(rmse),
        "MAE": float(mae),
        "n_samples_used": int(min_len)
    }
