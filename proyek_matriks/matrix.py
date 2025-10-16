class Matrix:
    """
    Kelas dasar untuk merepresentasikan matriks dan operasi dasarnya.
    File ini TIDAK BOLEH mengimpor modul lain dari proyek ini.
    """
    def __init__(self, data):
        if data and not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Semua baris dalam matriks harus memiliki panjang yang sama.")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __repr__(self):
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    @staticmethod
    def create_identity(size):
        """Membuat matriks identitas berukuran size x size."""
        data = [[1 if i == j else 0 for j in range(size)] for i in range(size)]
        return Matrix(data)

    def __add__(self, other):
        """Menambahkan dua matriks (overload operator +)."""
        if self.rows != other.rows or self.cols != other.cols:
            raise ValueError("Matriks harus memiliki ukuran yang sama untuk dijumlahkan.")
        
        result_data = [[self.data[i][j] + other.data[i][j] for j in range(self.cols)] for i in range(self.rows)]
        return Matrix(result_data)
    
    def scalar_multiply(self, scalar):
        """Mengalikan matriks dengan sebuah skalar."""
        result_data = [[cell * scalar for cell in row] for row in self.data]
        return Matrix(result_data)

    def is_square(self):
        """Memeriksa apakah matriks berbentuk persegi."""
        return self.rows == self.cols

    def get_minor(self, i, j):
        """
        Menghasilkan matriks minor dengan menghapus baris i dan kolom j.
        """
        minor_data = [row[:j] + row[j+1:] for row_idx, row in enumerate(self.data) if row_idx != i]
        return Matrix(minor_data)

    def get_row(self, index):
        return self.data[index]

    def get_col(self, index):
        return [self.data[i][index] for i in range(self.rows)]

    def get_data(self):
        return self.data

