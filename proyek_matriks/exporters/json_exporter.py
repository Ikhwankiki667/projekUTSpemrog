import json

# --- PERUBAHAN KUNCI ---
# Gunakan impor relatif (..) untuk naik satu level ke direktori 'proyek_matriks'
from ..matrix import Matrix

class JSONExporter:
    def __init__(self, matrix):
        self.matrix = matrix

    def export(self, filename):
        """Mengekspor matriks ke format JSON."""
        with open(filename, 'w') as f:
            json.dump(self.matrix.get_data(), f, indent=4)
        print(f"Matriks berhasil diekspor ke {filename}")
