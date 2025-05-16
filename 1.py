import sys
import numpy as np
from PyQt5.QtWidgets import (QApplication, QWidget, QVBoxLayout, 
                             QHBoxLayout, QSlider, QLabel)
from PyQt5.QtCore import Qt
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from scipy.integrate import odeint


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
    return X, Y, DX, DY
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

# nu = 10
def system(state, nu=2):
            x, y = state
            dx_dt = nu + x*x
            dy_dt = - y
            return [dx_dt, dy_dt]
class PlotApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # Создаем основные layout
        main_layout = QHBoxLayout()
        control_layout = QVBoxLayout()

        # Создаем слайдеры и метки для параметров
        self.a_slider = QSlider(Qt.Horizontal)
        self.a_slider.setRange(1, 10)
        self.a_label = QLabel("Amplitude: 1")
        
        self.k_slider = QSlider(Qt.Horizontal)
        self.k_slider.setStyleSheet("""
            QSlider{
                background: #E3DEE2;
            }
            QSlider::groove:horizontal {  
                height: 10px;
                margin: 0px;
                border-radius: 5px;
                background: #B0AEB1;
            }
            QSlider::handle:horizontal {
                background: #fff;
                border: 1px solid #E3DEE2;
                width: 17px;
                margin: -5px 0; 
                border-radius: 8px;
            }
            QSlider::sub-page:qlineargradient {
                background: #3B99FC;
                border-radius: 5px;
            }
        """)
        self.k_slider.setRange(10, 100)
        self.k_label = QLabel("Frequency: 1")
        
        self.phi_slider = QSlider(Qt.Horizontal)
        self.phi_slider.setRange(0, 360)
        self.phi_label = QLabel("Phase: 0")

        # Добавляем элементы управления в layout
        control_layout.addWidget(self.a_label)
        control_layout.addWidget(self.a_slider)
        control_layout.addWidget(self.k_label)
        control_layout.addWidget(self.k_slider)
        control_layout.addWidget(self.phi_label)
        control_layout.addWidget(self.phi_slider)

        # Создаем область для графика
        self.figure, self.ax = plt.subplots()
        self.canvas = FigureCanvas(self.figure)
        self.x = np.linspace(0, 2*np.pi, 1000)

        
        initial_state = [0, 0]
        t = np.linspace(0, 10, 1000)
        linear_states = []
        # linear_states= (odeint(lambda state, t: system(state), initial_state, t))

        initial_state2 = [0.2, 0.2]
        t2 = np.linspace(0, 10, 1000)
        linear_states2 = []
        # linear_states2= (odeint(lambda state, t: system(state), initial_state2, t2))
        
        # axs[0]
        self.line, = self.ax.plot(linear_states[:, 0], linear_states[:, 1])  # Начальный график
        self.line, = self.ax.streamplot(plot_saddle_node(0.5))  # Начальный график

        # Добавляем элементы в главный layout
        main_layout.addLayout(control_layout)
        main_layout.addWidget(self.canvas)

        self.setLayout(main_layout)

        # Подключаем сигналы
        self.a_slider.valueChanged.connect(self.update_plot)
        self.k_slider.valueChanged.connect(self.update_plot)
        self.phi_slider.valueChanged.connect(self.update_plot)
        
        # Обновление меток
        self.a_slider.valueChanged.connect(
            lambda: self.a_label.setText(f"Amplitude: {self.a_slider.value()}"))
        self.k_slider.valueChanged.connect(
            lambda: self.k_label.setText(f"Frequency: {self.k_slider.value()}"))
        self.phi_slider.valueChanged.connect(
            lambda: self.phi_label.setText(f"Phase: {self.phi_slider.value()}"))

        # Настройки окна
        self.setWindowTitle('Graph Plotter with Sliders')
        self.show()

    # def update_plot(self):
    #         # Получаем значения из слайдеров
    #         A = self.a_slider.value()
    #         k = self.k_slider.value()
    #         phi = self.phi_slider.value() * np.pi / 180  # Преобразуем в радианы

    #         # Обновляем данные графика
    #         y = A * np.sin(k * self.x + phi)
    #         self.line.set_ydata(y)

    #         # Обновляем границы и перерисовываем график
    #         self.ax.relim()
    #         self.ax.autoscale_view()
    #         self.canvas.draw()

    def update_plot(self):
        # Получаем значения из слайдеров
        A = self.a_slider.value()
        k = self.k_slider.value()
        phi = self.phi_slider.value() * np.pi / 180  # Преобразуем в радианы
        
        # Обновляем данные графика
        initial_state = [0, 0]

        t = np.linspace(0, 10, 1000)
        linear_states = []
        linear_states= (odeint(lambda state, t: system(state, k), initial_state, t))
        y = linear_states
        self.line.set_ydata(y[:, 0])
        
        # Обновляем границы и перерисовываем график
        self.ax.relim()
        self.ax.autoscale_view()
        self.canvas.draw()


if __name__ == '__main__':
    try:
        app = QApplication(sys.argv)
        ex = PlotApp()
        sys.exit(app.exec_())
    except:
         print("Преобразование прошло неудачно")