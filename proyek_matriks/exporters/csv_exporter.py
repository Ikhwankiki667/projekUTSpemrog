import csv

# --- PERUBAHAN KUNCI ---
# Gunakan impor relatif (..) untuk naik satu level ke direktori 'proyek_matriks'
from ..matrix import Matrix

def export_to_csv(matrix, filename):
    """
    Mengekspor data matriks ke sebuah file CSV.
    """
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(matrix.get_data())
    print(f"Matriks berhasil diekspor ke file {filename}")
