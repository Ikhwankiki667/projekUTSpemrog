import csv
# Impor relatif yang benar: naik satu level ke 'proyek_matriks' lalu cari 'matrix'
from ..matrix import Matrix

class CSVImporter:
    """
    Kelas untuk mengimpor data matriks dari file CSV.
    """
    def __init__(self, filepath):
        self.filepath = filepath

    def import_data(self):
        """Membaca file CSV dan mengembalikannya sebagai list dari list float."""
        matrix_data = []
        try:
            with open(self.filepath, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                # Lewati baris pertama (header)
                next(reader, None)
                for row in reader:
                    # Konversi setiap sel menjadi float
                    if row: # Pastikan baris tidak kosong
                        matrix_data.append([float(cell) for cell in row])
        except FileNotFoundError:
            print(f"Error: File '{self.filepath}' tidak ditemukan.")
            return None
        except ValueError:
            print(f"Error: Tidak bisa mengubah data menjadi angka di '{self.filepath}'. Periksa nilai non-numerik.")
            return None
        return matrix_data

