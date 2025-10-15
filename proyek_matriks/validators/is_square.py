# proyek_matriks/validators/is_identity.py
from matrix import Matrix

def is_square(matrix: Matrix) -> bool:
    """Memeriksa apakah matriks adalah matriks persegi."""
    return matrix.rows == matrix.cols
