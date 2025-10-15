# --- PERUBAHAN KUNCI ---
# Gunakan impor relatif (..) untuk naik satu level ke direktori 'proyek_matriks'
from ..matrix import Matrix

def multiply_matrices(matrix1, matrix2):
    """
    Mengalikan dua matriks.
    """
    if matrix1.cols != matrix2.rows:
        raise ValueError("Jumlah kolom matriks pertama harus sama dengan jumlah baris matriks kedua.")

    result_data = []
    for i in range(matrix1.rows):
        row = []
        for j in range(matrix2.cols):
            # Hitung dot product dari baris matrix1 dan kolom matrix2
            dot_product = sum(matrix1.get_data()[i][k] * matrix2.get_data()[k][j] for k in range(matrix1.cols))
            row.append(dot_product)
        result_data.append(row)

    return Matrix(result_data)
