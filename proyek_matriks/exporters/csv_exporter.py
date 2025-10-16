# importers/csv_importer.py

import csv

class CSVImporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def import_data(self):
        """Mengimpor data numerik dari CSV."""
        try:
            data = []
            with open(self.file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Skip header
                
                for row in reader:
                    if len(row) >= 3:  # Pastikan ada 3 kolom
                        try:
                            # Konversi ke float
                            numeric_row = [float(row[0]), float(row[1]), float(row[2])]
                            data.append(numeric_row)
                        except ValueError:
                            continue  # Lewati baris tidak valid
            
            return data if data else None
            
        except Exception as e:
            print(f"ERROR mengimpor CSV: {e}")
            return None