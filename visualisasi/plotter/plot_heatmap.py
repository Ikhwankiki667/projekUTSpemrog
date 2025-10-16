# visualisasi/plotter/plot_heatmap.py

import matplotlib.pyplot as plt
import seaborn as sns

def create_correlation_heatmap(df, output_dir):
    """Buat heatmap korelasi"""
    correlation_matrix = df.corr()
    
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation_matrix, annot=True, cmap='coolwarm', center=0, square=True, linewidths=0.5)
    plt.title('Correlation Heatmap')
    plt.tight_layout()
    
    png_path = os.path.join(output_dir, 'correlation_heatmap.png')
    plt.savefig(png_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"[SUCCESS] Correlation Heatmap disimpan di: {png_path}")