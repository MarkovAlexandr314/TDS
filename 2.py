import numpy as np
import matplotlib.pyplot as plt
from ipywidgets import interact, FloatSlider


def update_saddle_node(mu, y_sign=-1):
    """Обновление графика седло-узла"""
    plt.figure(figsize=(12, 5))
    
    # Седло-узел
    plt.subplot(1, 2, 1)
    x = np.linspace(-3, 3, 30)
    y = np.linspace(-1.5, 1.5, 20)
    X, Y = np.meshgrid(x, y)
    
    DX = mu + X**2
    DY = y_sign * Y
    
    plt.streamplot(X, Y, DX, DY, color='gray', density=1.5)
    
    # Точки равновесия
    if mu < 0:
        plt.plot(-np.sqrt(-mu), 0, 'go', markersize=10, label='Устойчивый узел')
        plt.plot(np.sqrt(-mu), 0, 'ro', markersize=10, label='Седло')
    elif mu == 0:
        plt.plot(0, 0, 'o', color='orange', markersize=10, label='Седло-узел')
    
    plt.title(f"Седло-узел ($\mu = {mu:.2f}$)")
    plt.xlim(-3, 3)
    plt.ylim(-1.5, 1.5)
    plt.legend()

def update_pitchfork(mu):
    """Обновление графика вилки"""
    plt.subplot(1, 2, 2)
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-1, 1, 20)
    X, Y = np.meshgrid(x, y)
    
    DX = mu*X - X**3
    DY = -Y
    
    plt.streamplot(X, Y, DX, DY, color='gray', density=1.5)
    
    # Точки равновесия
    if mu <= 0:
        plt.plot(0, 0, 'go', markersize=10, label='Устойчивый узел')
    else:
        plt.plot(0, 0, 'ro', markersize=10, label='Седло')
        plt.plot(np.sqrt(mu), 0, 'go', markersize=10)
        plt.plot(-np.sqrt(mu), 0, 'go', markersize=10)
    
    plt.title(f"Вилка ($\mu = {mu:.2f}$)")
    plt.xlim(-2, 2)
    plt.ylim(-1, 1)
    plt.legend()
    plt.tight_layout()

@interact(mu=FloatSlider(
    value=0.0,
    min=-1.0,
    max=1.0,
    step=0.1,
    description='μ parameter:',
    continuous_update=False
))
def update_plots(mu):
    plt.close('all')
    update_saddle_node(mu)
    update_pitchfork(mu)
    plt.show()