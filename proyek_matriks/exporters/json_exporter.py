# exporters/json_exporter.py
import json
import os

class JSONExporter:
    def __init__(self, output_file):
        self.output_file = output_file

    def export(self, regression):
        results = regression.get_results()
        output_data = {
            "beta_coefficients": results["beta_coefficients"],
            "predicted_y": results["predicted_y"]
        }
        
        # Pastikan direktori output ada
        os.makedirs(os.path.dirname(self.output_file), exist_ok=True)
        
        # Format output sesuai dengan yang diharapkan visualizer.py
        output_data = {
            "beta": results["beta_coefficients"],
            "y_pred": results["predicted_y"]
        }
        
        print(f"DEBUG: Jumlah beta: {len(output_data['beta'])}")
        print(f"DEBUG: Jumlah prediksi: {len(output_data['y_pred'])}")
        
        with open(self.output_file, 'w', encoding='utf-8') as f:
            json.dump(output_data, f, indent=4)