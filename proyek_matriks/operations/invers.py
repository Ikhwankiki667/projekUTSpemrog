from ..matrix import Matrix
from .determinant import determinant
from .transpose import transpose

def get_minor(matrix, i, j):
    """
    Fungsi bantuan untuk mendapatkan minor dari sebuah matriks
    dengan menghapus baris i dan kolom j.
    """
    minor_data = [row[:j] + row[j+1:] for row in (matrix.data[:i] + matrix.data[i+1:])]
    return Matrix(minor_data)

def invers(matrix):
    """
    Menghitung invers dari sebuah matriks persegi.
    Menggunakan metode matriks adjoin.
    """
    if matrix.rows != matrix.cols:
        raise ValueError("Matriks harus persegi untuk diinvers.")

    det = determinant(matrix)
    if det == 0:
        raise ValueError("Matriks singular, tidak dapat diinvers (determinan adalah nol).")

    # Kasus khusus untuk matriks 2x2 untuk efisiensi
    if matrix.rows == 2:
        a, b = matrix.data[0]
        c, d = matrix.data[1]
        inv_det = 1 / det
        invers_data = [[d * inv_det, -b * inv_det], [-c * inv_det, a * inv_det]]
        return Matrix(invers_data)

    # Menghitung matriks kofaktor untuk ukuran > 2x2
    cofactors = []
    for r in range(matrix.rows):
        cofactor_row = []
        for c in range(matrix.cols):
            minor = get_minor(matrix, r, c)
            cofactor = ((-1)**(r + c)) * determinant(minor)
            cofactor_row.append(cofactor)
        cofactors.append(cofactor_row)
    
    cofactor_matrix = Matrix(cofactors)

    # Adjoin adalah transpose dari matriks kofaktor
    adjoin_matrix = transpose(cofactor_matrix)

    # Invers adalah adjoin dibagi dengan determinan
    invers_data = [[elem / det for elem in row] for row in adjoin_matrix.data]

    return Matrix(invers_data)

