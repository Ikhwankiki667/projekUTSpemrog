# --- PERUBAHAN KUNCI ---
# Gunakan impor relatif (..) untuk naik satu level ke direktori 'proyek_matriks'
from ..matrix import Matrix

def transpose(matrix):
    """
    Menghitung transpose dari sebuah matriks.
    """
    transposed_data = []
    for j in range(matrix.cols):
        row = []
        for i in range(matrix.rows):
            row.append(matrix.get_data()[i][j])
        transposed_data.append(row)
    
    return Matrix(transposed_data)
