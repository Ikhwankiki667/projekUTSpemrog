import plotly.graph_objects as go
import numpy as np

def plot_3d(X, y_true, beta, output_path):
    """
    Membuat plot 3D interaktif yang menunjukkan titik data dan bidang regresi.
    Hanya berfungsi jika ada tepat 2 fitur di X.

    Args:
        X (list of lists): Data fitur (harus 2 kolom).
        y_true (list): Nilai target asli.
        beta (list of lists): Koefisien regresi.
        output_path (str): Path untuk menyimpan file plot HTML.
    """
    x1 = [row[1] for row in X]  # Fitur pertama (indeks 1, karena indeks 0 adalah intercept)
    x2 = [row[2] for row in X]  # Fitur kedua

    # Buat scatter plot dari titik data asli
    fig = go.Figure(data=[go.Scatter3d(
        x=x1,
        y=x2,
        z=y_true,
        mode='markers',
        marker=dict(size=5, color='blue', opacity=0.8),
        name='Titik Data Aktual'
    )])

    # Buat meshgrid untuk bidang regresi
    x1_range = np.linspace(min(x1), max(x1), 10)
    x2_range = np.linspace(min(x2), max(x2), 10)
    x1_mesh, x2_mesh = np.meshgrid(x1_range, x2_range)
    
    # Hitung nilai z (harga rumah prediksi) untuk setiap titik di meshgrid
    # Persamaan: z = b0*1 + b1*x1 + b2*x2
    b0 = beta[0][0]
    b1 = beta[1][0]
    b2 = beta[2][0]
    z_mesh = b0 + b1 * x1_mesh + b2 * x2_mesh

    # Tambahkan bidang regresi ke plot
    fig.add_trace(go.Surface(
        x=x1_range,
        y=x2_range,
        z=z_mesh,
        opacity=0.7,
        colorscale='Viridis',
        showscale=False,
        name='Bidang Regresi'
    ))

    fig.update_layout(
        title='Visualisasi Bidang Regresi 3D',
        scene=dict(
            xaxis_title='Fitur 1 (e.g., Luas Tanah)',
            yaxis_title='Fitur 2 (e.g., Jumlah Kamar)',
            zaxis_title='Target (Harga Rumah)'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )

    fig.write_html(output_path)

