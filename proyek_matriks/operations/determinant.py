# --- PERUBAHAN KUNCI ---
# Gunakan impor relatif (..) untuk naik satu level ke direktori 'proyek_matriks'
from ..matrix import Matrix

def determinant(matrix):
    """
    Menghitung determinan dari sebuah matriks persegi.
    """
    if not matrix.is_square():
        raise ValueError("Matriks harus persegi untuk dihitung determinannya.")

    # Kasus dasar untuk matriks 1x1
    if matrix.rows == 1:
        return matrix.get_data()[0][0]

    # Kasus dasar untuk matriks 2x2
    if matrix.rows == 2:
        a, b = matrix.get_row(0)
        c, d = matrix.get_row(1)
        return a * d - b * c

    # Rekursif untuk matriks yang lebih besar (ekspansi kofaktor)
    det = 0
    for c in range(matrix.cols):
        minor = matrix.get_minor(0, c)
        # Tambah atau kurangi berdasarkan posisi kolom
        det += ((-1)**c) * matrix.get_data()[0][c] * determinant(minor)
    
    return det
