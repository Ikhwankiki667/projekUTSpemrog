import plotly.graph_objects as go
import os
import numpy as np

def plot_regression_3d(x1, x2, y_true, y_pred):
    """
    Membuat dan menyimpan plot regresi 3D, termasuk bidang regresi.
    """
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', 'plots')
    os.makedirs(output_dir, exist_ok=True)
    
    fig = go.Figure()

    # 1. Tambahkan scatter plot untuk data aktual
    fig.add_trace(go.Scatter3d(
        x=x1, y=x2, z=y_true, 
        mode='markers', 
        name='Data Aktual',
        marker=dict(size=4, color='blue', opacity=0.8)
    ))

    # 2. Buat meshgrid untuk menggambar bidang regresi
    # Ini adalah cara yang benar untuk membuat permukaan di 3D
    x1_range = np.linspace(x1.min(), x1.max(), 10)
    x2_range = np.linspace(x2.min(), x2.max(), 10)
    x1_mesh, x2_mesh = np.meshgrid(x1_range, x2_range)

    # Kita perlu model linear untuk memprediksi nilai z pada mesh
    # y = b0 + b1*x1 + b2*x2. Kita bisa estimasi ini dari y_pred
    A = np.c_[np.ones(len(x1)), x1, x2]
    beta, _, _, _ = np.linalg.lstsq(A, y_pred, rcond=None)
    
    # Hitung nilai Z (target) untuk setiap titik di mesh
    z_plane = beta[0] + beta[1] * x1_mesh + beta[2] * x2_mesh
    
    # 3. Tambahkan permukaan/bidang regresi ke plot
    fig.add_trace(go.Surface(
        x=x1_range,
        y=x2_range,
        z=z_plane,
        colorscale='Viridis',
        opacity=0.5,
        showscale=False,
        name='Bidang Regresi'
    ))

    fig.update_layout(
        title='Regresi Linear 3D dengan Bidang Prediksi', 
        scene=dict(
            xaxis_title=x1.name if hasattr(x1, 'name') else 'Fitur 1', 
            yaxis_title=x2.name if hasattr(x2, 'name') else 'Fitur 2', 
            zaxis_title=y_true.name if hasattr(y_true, 'name') else 'Target'
        ),
        margin=dict(l=0, r=0, b=0, t=40)
    )
    
    output_path = os.path.join(output_dir, 'regression_plot_3d.html')
    fig.write_html(output_path)
    print(f"Plot 3D berhasil disimpan di {output_path}")
