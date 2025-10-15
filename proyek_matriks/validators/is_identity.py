# proyek_matriks/validators/is_identity.py
from matrix import Matrix

def is_identity(matrix: Matrix) -> bool:
    if matrix.rows != matrix.cols:
        return False
    for i in range(matrix.rows):
        for j in range(matrix.cols):
            if i == j and matrix.data[i][j] != 1:
                return False
            if i != j and matrix.data[i][j] != 0:
                return False
    return True
