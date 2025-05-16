import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from scipy.integrate import odeint

class LorenzApp(tk.Tk):
    def __init__(self):
        super().__init__()
        
        # Параметры системы
        self.sigma = 10.0
        self.beta = 1.0
        self.rho = 28.0
        self.t = np.linspace(0, 40, 4000)
        self.initial_state = [1.0, 1.0, 1.0]
        
        # Настройка интерфейса
        self.title("Конвективная петля Лоренца")
        self.geometry("800x600")
        
        # Создание виджетов
        self.create_widgets()
        
    def create_widgets(self):
        # Фрейм для управления
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Слайдер для параметра rho
        self.rho_slider = ttk.Scale(
            control_frame,
            from_=0.1,
            to=50.0,
            value=self.rho,
            orient=tk.HORIZONTAL,
            command=self.update_rho
        )
        ttk.Label(control_frame, text="Интенсивность подогрева (ρ):").pack()
        self.rho_slider.pack(fill=tk.X, pady=5)
        
        # Метка для отображения значения
        self.rho_value = ttk.Label(control_frame, text=f"ρ = {self.rho:.2f}")
        self.rho_value.pack(pady=5)
        
        # Кнопка обновления
        ttk.Button(control_frame, text="Обновить", command=self.update_plot).pack(pady=10)
        
        # График
        self.fig = Figure(figsize=(6, 6))
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # Инициализация scatter и colorbar
        self.sc = None
        self.cbar = None
        
        # Первоначальное построение
        self.update_plot()
    
    def lorenz_system(self, state, t):
        x, y, z = state
        dxdt = self.sigma * (y - x)
        dydt = x * (self.rho - z) - y
        dzdt = x * y - self.beta * z
        return [dxdt, dydt, dzdt]
    
    def update_rho(self, value):
        self.rho = float(value)
        self.rho_value.config(text=f"ρ = {self.rho:.2f}")
    
    def update_plot(self):
        # Решение уравнений
        solution = odeint(self.lorenz_system, self.initial_state, self.t)
        x, y, z = solution.T
        
        # Очистка предыдущего графика
        self.ax.clear()
        
        # Настройка осей
        self.ax.set_xlim((-25, 25))
        self.ax.set_ylim((-35, 35))
        self.ax.set_zlim((0, 50))
        self.ax.set_xlabel("X Axis")
        self.ax.set_ylabel("Y Axis")
        self.ax.set_zlabel("Z Axis")
        
        # Построение графика
        self.sc = self.ax.scatter(x, y, z, c=z, cmap='plasma', s=2)
        
        # Обновление или создание цветовой шкалы
        if self.cbar:
            self.cbar.update_normal(self.sc)
        else:
            self.cbar = self.fig.colorbar(self.sc, ax=self.ax, label='Температура (z)')
        
        self.ax.set_title(f'Конвективная петля (ρ = {self.rho:.2f})')
        
        # Обновление холста
        self.canvas.draw()

if __name__ == "__main__":
    app = LorenzApp()
    app.mainloop()