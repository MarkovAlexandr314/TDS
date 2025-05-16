import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class BifurcationApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        self.title("Бифуркационные диаграммы")
        self.geometry("1000x600")
        
        # Параметры модели
        self.mu = 0.0
        self.y_sign = -1
        
        # Создание виджетов
        self.create_widgets()
        self.init_plots()
        
    def create_widgets(self):
        # Фрейм для графиков
        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True)
        
        # Слайдер для параметра mu
        self.slider_frame = ttk.Frame(self)
        self.slider_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.mu_slider = ttk.Scale(
            self.slider_frame,
            from_=-1.0,
            to=1.0,
            value=self.mu,
            orient=tk.HORIZONTAL,
            command=self.update_mu
        )
        self.mu_slider.pack(fill=tk.X, expand=True)
        
        self.mu_label = ttk.Label(self.slider_frame, text="μ = 0.00")
        self.mu_label.pack()
        
        # Настройка событий для плавного обновления
        self.mu_slider.bind("<ButtonRelease-1>", self.update_plots)
        
    def init_plots(self):
        # Создание фигуры Matplotlib
        self.fig = Figure(figsize=(10, 5))
        self.ax1 = self.fig.add_subplot(121)
        self.ax2 = self.fig.add_subplot(122)
        
        # Настройка холста
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.plot_frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        # Первоначальная отрисовка
        self.update_plots()
    
    def update_mu(self, value):
        self.mu = float(value)
        self.mu_label.config(text=f"μ = {self.mu:.2f}")
    
    def update_saddle_node(self):
        self.ax1.clear()
        x = np.linspace(-3, 3, 30)
        y = np.linspace(-1.5, 1.5, 20)
        X, Y = np.meshgrid(x, y)
        
        DX = self.mu + X**2
        DY = self.y_sign * Y
        
        self.ax1.streamplot(X, Y, DX, DY, color='gray', density=1.5)
        
        if self.mu < 0:
            self.ax1.plot(-np.sqrt(-self.mu), 0, 'go', markersize=10, label='Устойчивый узел')
            self.ax1.plot(np.sqrt(-self.mu), 0, 'ro', markersize=10, label='Седло')
        elif self.mu == 0:
            self.ax1.plot(0, 0, 'o', color='orange', markersize=10, label='Седло-узел')
        
        self.ax1.set_title(f"Седло-узел ($\mu = {self.mu:.2f}$)")
        self.ax1.set_xlim(-3, 3)
        self.ax1.set_ylim(-1.5, 1.5)
        self.ax1.legend()
    
    def update_pitchfork(self):
        self.ax2.clear()
        x = np.linspace(-2, 2, 30)
        y = np.linspace(-1, 1, 20)
        X, Y = np.meshgrid(x, y)
        
        DX = self.mu*X - X**3
        DY = -Y
        
        self.ax2.streamplot(X, Y, DX, DY, color='gray', density=1.5)
        
        if self.mu <= 0:
            self.ax2.plot(0, 0, 'go', markersize=10, label='Устойчивый узел')
        else:
            self.ax2.plot(0, 0, 'ro', markersize=10, label='Седло')
            self.ax2.plot(np.sqrt(self.mu), 0, 'go', markersize=10)
            self.ax2.plot(-np.sqrt(self.mu), 0, 'go', markersize=10)
        
        self.ax2.set_title(f"Вилка ($\mu = {self.mu:.2f}$)")
        self.ax2.set_xlim(-2, 2)
        self.ax2.set_ylim(-1, 1)
        self.ax2.legend()
    
    def update_plots(self, event=None):
        self.update_saddle_node()
        self.update_pitchfork()
        self.fig.tight_layout()
        self.canvas.draw()

if __name__ == "__main__":
    app = BifurcationApp()
    app.mainloop()