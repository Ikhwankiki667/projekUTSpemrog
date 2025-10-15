# proyek_matriks/validators/is_identity.py
from matrix import Matrix

def is_square(matrix: Matrix) -> bool:
    """matriks persegi?"""
    return matrix.rows == matrix.cols

def is_symmetric(matrix: Matrix) -> bool:
    """matriks simetris?"""
    if not is_square(matrix):
        return False
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if matrix.data[i][j] != matrix.data[j][i]:
                return False
    return True
