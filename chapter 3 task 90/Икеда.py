import tkinter as tk
from tkinter import ttk
import numpy as np
import cmath
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class IkedaAppRealParams:
    def __init__(self, master):
        self.master = master
        self.master.title("Система Икеды (A и B действительные)")
        self.setup_variables()
        self.create_widgets()
        self.generate_points()

    def setup_variables(self):
        """Инициализация переменных управления"""
        self.A = tk.DoubleVar(value=1.0)
        self.B = tk.DoubleVar(value=0.9)
        self.grid_size = tk.IntVar(value=20)
        self.iterations = tk.IntVar(value=50)
        self.center_x = tk.DoubleVar(value=0.0)
        self.center_y = tk.DoubleVar(value=0.0)
        self.width = tk.DoubleVar(value=4.0)
        self.height = tk.DoubleVar(value=4.0)
        self.points = None
        self.current_iter = 0
        self.anim_running = False

    def create_widgets(self):
        """Создание элементов интерфейса"""
        control_frame = ttk.Frame(self.master, padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Поля ввода параметров
        ttk.Label(control_frame, text="A (действительное):").pack()
        ttk.Entry(control_frame, textvariable=self.A).pack()
        
        ttk.Label(control_frame, text="B (действительное):").pack()
        ttk.Entry(control_frame, textvariable=self.B).pack()

        ttk.Label(control_frame, text="Размер сетки:").pack()
        ttk.Entry(control_frame, textvariable=self.grid_size).pack()

        ttk.Label(control_frame, text="Итерации:").pack()
        ttk.Entry(control_frame, textvariable=self.iterations).pack()

        ttk.Label(control_frame, text="Центр X:").pack()
        ttk.Entry(control_frame, textvariable=self.center_x).pack()

        ttk.Label(control_frame, text="Центр Y:").pack()
        ttk.Entry(control_frame, textvariable=self.center_y).pack()

        ttk.Label(control_frame, text="Ширина:").pack()
        ttk.Entry(control_frame, textvariable=self.width).pack()

        ttk.Label(control_frame, text="Высота:").pack()
        ttk.Entry(control_frame, textvariable=self.height).pack()

        # Кнопки управления
        ttk.Button(control_frame, text="Обновить", command=self.generate_points).pack(pady=5)
        ttk.Button(control_frame, text="Старт", command=self.start_animation).pack(pady=5)
        ttk.Button(control_frame, text="Стоп", command=self.stop_animation).pack(pady=5)
        ttk.Button(control_frame, text="Сброс", command=self.reset).pack(pady=5)

        # Настройка графика
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)

    def generate_points(self):
        """Генерация начального облака точек"""
        size = self.grid_size.get()
        x = np.linspace(
            self.center_x.get() - self.width.get()/2,
            self.center_x.get() + self.width.get()/2,
            size
        )
        y = np.linspace(
            self.center_y.get() - self.height.get()/2,
            self.center_y.get() + self.height.get()/2,
            size
        )
        X, Y = np.meshgrid(x, y)
        self.points = X.flatten() + 1j*Y.flatten()
        self.current_iter = 0
        self.update_plot()

    def iterate_system(self):
        """Одна итерация системы Икеды"""
        A = self.A.get()
        B = self.B.get()
        self.points = A + B * self.points * np.exp(1j * np.abs(self.points)**2)
        self.current_iter += 1

    def update_plot(self):
        """Обновление графика"""
        self.ax.clear()
        self.ax.scatter(np.real(self.points), np.imag(self.points), s=1, c='blue')
        self.ax.set_title(f'Итерация: {self.current_iter}')
        self.ax.set_xlim(-5, 5)
        self.ax.set_ylim(-5, 5)
        self.canvas.draw()

    def start_animation(self):
        """Запуск анимации"""
        if not self.anim_running:
            self.anim_running = True
            self.animate()

    def stop_animation(self):
        """Остановка анимации"""
        self.anim_running = False

    def animate(self):
        """Шаг анимации"""
        if self.anim_running and self.current_iter < self.iterations.get():
            self.iterate_system()
            self.update_plot()
            self.master.after(50, self.animate)
        else:
            self.anim_running = False

    def reset(self):
        """Сброс параметров"""
        self.A.set(1.0)
        self.B.set(0.9)
        self.grid_size.set(20)
        self.iterations.set(50)
        self.center_x.set(0.0)
        self.center_y.set(0.0)
        self.width.set(4.0)
        self.height.set(4.0)
        self.generate_points()

if __name__ == "__main__":
    root = tk.Tk()
    app = IkedaAppRealParams(root)
    root.mainloop()