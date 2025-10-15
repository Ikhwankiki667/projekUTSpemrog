# proyek_matriks/utilities.py
from matrix import Matrix
import random

def print_matrix(matrix: Matrix):
    for row in matrix.data:
        print(row)

def same_shape(m1: Matrix, m2: Matrix) -> bool:
    """Cek apakah dua matriks punya bentuk sama."""
    return m1.rows == m2.rows and m1.cols == m2.cols

def can_multiply(m1: Matrix, m2: Matrix) -> bool:
    """Cek apakah dua matriks bisa dikalikan (kolom m1 = baris m2)."""
    return m1.cols == m2.rows

def make_compatible_matrix_like(reference: Matrix) -> Matrix:
    """
    Buat matriks baru yang punya ukuran sama dengan reference matrix.
    Diisi nilai acak sederhana agar operasi tetap bisa berjalan.
    """
    rows, cols = reference.rows, reference.cols
    new_data = [[random.randint(1, 9) for _ in range(cols)] for _ in range(rows)]
    return Matrix(new_data)
