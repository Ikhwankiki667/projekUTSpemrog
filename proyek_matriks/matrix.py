class matrix:
    """
    Kelas dasar untuk merepresentasikan matriks dan operasi dasarnya.
    File ini TIDAK BOLEH mengimpor modul lain dari proyek ini.
    """
    def __init__(self, data):
        # Memastikan semua baris memiliki panjang yang sama
        if data and not all(len(row) == len(data[0]) for row in data):
            raise ValueError("Semua baris dalam matriks harus memiliki panjang yang sama.")
        self.data = data
        self.rows = len(data)
        self.cols = len(data[0]) if self.rows > 0 else 0

    def __repr__(self):
        """Representasi string dari matriks untuk printing."""
        return "\n".join(["\t".join(map(str, row)) for row in self.data])

    def get_row(self, index):
        """Mengembalikan satu baris dari matriks."""
        return self.data[index]

    def get_col(self, index):
        """Mengembalikan satu kolom dari matriks."""
        return [self.data[i][index] for i in range(self.rows)]

    def get_data(self):
        """Mengembalikan data matriks sebagai list dari list."""
        return self.data
