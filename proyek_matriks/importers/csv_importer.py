# importers/csv_importer.py
import csv

class CSVImporter:
    def __init__(self, file_path):
        self.file_path = file_path

    def import_data(self):
        """Mengimpor data dari file CSV dan mengonversi ke angka."""
        try:
            data = []
            valid_rows = 0
            total_rows = 0
            
            with open(self.file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile)
                headers = next(reader)  # Skip header
                
                for row in reader:
                    total_rows += 1
                    try:
                        # Konversi setiap sel ke float
                        numeric_row = [float(cell.strip()) for cell in row if cell.strip()]
                        if len(numeric_row) >= 2:  # Minimal 1 fitur + 1 target
                            data.append(numeric_row)
                            valid_rows += 1
                        else:
                            print(f"WARNING: Baris {total_rows} dilewati - tidak cukup data numerik")
                    except ValueError as e:
                        print(f"WARNING: Baris {total_rows} dilewati - data tidak valid: {row}")
                        continue
            
            print(f"INFO: Dari {total_rows} baris, {valid_rows} baris valid diproses")
            return data if data else None
            
        except Exception as e:
            print(f"ERROR saat mengimpor CSV: {e}")
            return None