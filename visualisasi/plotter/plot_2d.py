import plotly.graph_objects as go
import os
import numpy as np

def plot_regression_2d(y_true, y_pred):
    """
    Membuat dan menyimpan plot regresi 2D (scatter plot dengan garis regresi).
    """
    output_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'outputs', 'plots')
    os.makedirs(output_dir, exist_ok=True)
    
    fig = go.Figure()

    # Tambahkan scatter plot untuk data aktual
    fig.add_trace(go.Scatter(
        x=y_true, 
        y=y_pred, 
        mode='markers', 
        name='Data Aktual vs. Prediksi',
        marker=dict(color='blue', opacity=0.7)
    ))

    # Tambahkan garis ideal (y_true = y_pred) untuk perbandingan
    # Garis ini menunjukkan prediksi yang sempurna
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    fig.add_trace(go.Scatter(
        x=[min_val, max_val], 
        y=[min_val, max_val], 
        mode='lines', 
        name='Garis Ideal (Prediksi Sempurna)',
        line=dict(color='red', dash='dash')
    ))

    fig.update_layout(
        title='Perbandingan Nilai Aktual dan Prediksi',
        xaxis_title='Nilai Aktual (y_true)',
        yaxis_title='Nilai Prediksi (y_pred)',
        showlegend=True
    )
    
    output_path = os.path.join(output_dir, 'regression_plot_2d.html')
    fig.write_html(output_path)
    print(f"Plot 2D berhasil disimpan di {output_path}")
