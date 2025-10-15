import os
import seaborn as sns
import matplotlib.pyplot as plt

# --- PERUBAHAN KUNCI ---
# Nama fungsi diubah dari 'create_heatmap' menjadi 'plot_heatmap'
# agar cocok dengan panggilan import di visualizer.py
def plot_heatmap(df):
    """
    Membuat dan menyimpan plot heatmap dari korelasi antar kolom dalam DataFrame.
    """
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', 'plots')
    os.makedirs(output_dir, exist_ok=True)
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(df.corr(), annot=True, cmap='coolwarm', fmt=".2f")
    plt.title('Heatmap Korelasi Fitur')
    
    # Simpan plot ke file
    output_path = os.path.join(output_dir, 'regression_heatmap.png')
    plt.savefig(output_path)
    plt.close() # Tutup plot agar tidak ditampilkan di environment non-interaktif
    print(f"Heatmap berhasil disimpan di {output_path}")
