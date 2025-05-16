import numpy as np
import matplotlib.pyplot as plt

# Настройка стиля графиков
# plt.style.use('seaborn')

def plot_saddle_node(mu, y_sign=-1, ax=None):
    """
    Бифуркация седло-узел:
    - mu: параметр бифуркации
    - y_sign: -1 (устойчивый узел) или 1 (неустойчивый узел)
    """
    # Создаем сетку
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-1, 1, 20)
    X, Y = np.meshgrid(x, y)
    
    # Динамика системы
    DX = mu + X**2
    DY = y_sign * Y
    
    # Точки равновесия
    eq_points = []
    if mu < 0:
        eq_points.append((-np.sqrt(-mu), 0))  # Устойчивый узел (зеленый)
        eq_points.append((np.sqrt(-mu), 0))   # Седло (красный)
    elif mu == 0:
        eq_points.append((0, 0))              # Седло-узел (оранжевый)

    # Построение фазового портрета
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.streamplot(X, Y, DX, DY, color='gray', density=1.5)
    
    # Рисуем точки равновесия
    for (x, y) in eq_points:
        if x == np.sqrt(-mu) and mu < 0:
            ax.plot(x, y, 'ro', markersize=8, label='Седло')  # Седло
        else:
            ax.plot(x, y, 'go', markersize=8, label='Узел')   # Узел
    if mu == 0:
        ax.plot(0, 0, 'o', color='orange', markersize=8, label='Седло-узел')
    return ax

def plot_pitchfork(mu, ax=None):
    """
    Бифуркация вилка:
    - mu: параметр бифуркации
    """
    # Создаем сетку
    x = np.linspace(-2, 2, 30)
    y = np.linspace(-1, 1, 20)
    X, Y = np.meshgrid(x, y)
    
    # Динамика системы
    DX = mu*X - X**3
    DY = -Y
    
    # Точки равновесия
    eq_points = []
    if mu <= 0:
        eq_points.append((0, 0))                     # Устойчивый узел
    else:
        eq_points.append((0, 0))                     # Седло
        eq_points.append((np.sqrt(mu), 0))            # Устойчивые узлы
        eq_points.append((-np.sqrt(mu), 0))

    # Построение фазового портрета
    if ax is None:
        fig, ax = plt.subplots(figsize=(6, 4))
    
    ax.streamplot(X, Y, DX, DY, color='gray', density=1.5)
    
    # Рисуем точки равновесия
    for (x, y) in eq_points:
        if x == 0 and mu > 0:
            ax.plot(x, y, 'ro', markersize=8, label='Седло')
        else:
            ax.plot(x, y, 'go', markersize=8, label='Узел')
    
    ax.set_title(f"Вилка ($\mu = {mu}$)")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.grid(True)
    ax.legend()

# Построение графиков
fig, axes = plt.subplots(2, 3, figsize=(18, 10))

# Седло-узел (устойчивый узел)
plot_saddle_node(-0.5, ax=axes[0, 0])
plot_saddle_node(0, ax=axes[0, 1])
plot_saddle_node(0.5, ax=axes[0, 2])

# Вилка
plot_pitchfork(-0.5, ax=axes[1, 0])
plot_pitchfork(0, ax=axes[1, 1])
plot_pitchfork(0.5, ax=axes[1, 2])

plt.tight_layout()
plt.show()