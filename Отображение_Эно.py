import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class HenonApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Отображение Эно")
        self.geometry("1000x800")
        
        # Параметры системы
        self.λ = 1.4
        self.b = 0.3
        self.running = False
        self.points = self.generate_cloud()
        
        # Создание элементов интерфейса
        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        # Фрейм для управления
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Слайдеры параметров с метками значений
        self.λ_slider, self.λ_label = self.create_slider_with_label(
            control_frame, "λ:", 0.1, 2.0, self.λ)
        self.b_slider, self.b_label = self.create_slider_with_label(
            control_frame, "b:", 0.0, 1.2, self.b)
        
        # Кнопки управления
        self.btn_frame = ttk.Frame(control_frame)
        self.btn_frame.pack(pady=20)
        
        self.start_btn = ttk.Button(self.btn_frame, text="Старт", command=self.toggle_animation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(self.btn_frame, text="Сброс", command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def create_slider_with_label(self, parent, label, min_val, max_val, init_val):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        
        # Метка для отображения значения
        value_label = ttk.Label(frame, width=6)
        value_label.pack(side=tk.RIGHT)
        
        # Слайдер
        slider = ttk.Scale(frame, from_=min_val, to=max_val, value=init_val,
                          orient=tk.HORIZONTAL,
                          command=lambda v, lbl=value_label: lbl.config(text=f"{float(v):.2f}"))
        slider.pack(side=tk.RIGHT, expand=True, padx=5)
        
        # Инициализация значения
        value_label.config(text=f"{init_val:.2f}")
        
        return slider, value_label

    def setup_plot(self):
        # Настройка графика
        self.fig = Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-10, 10)
        self.ax.set_ylim(-10, 10)
        self.ax.set_title("Эволюция облака точек в отображении Эно")
        self.scat = self.ax.scatter(self.points[:,0], self.points[:,1], s=1, c='blue')
        
        # Встраивание графика в Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def generate_cloud(self, num=50):
        # Создание регулярной сетки точек
        x = np.linspace(-0.5, 0.5, num)
        y = np.linspace(-0.5, 0.5, num)
        X, Y = np.meshgrid(x, y)
        return np.column_stack((X.ravel(), Y.ravel()))

    def henon_map(self, points):
        x, y = points[:, 0], points[:, 1]
        new_x = 1 - self.λ * x**2 - self.b * y
        new_y = x
        print(self.λ, self.b)
        return np.column_stack((new_x, new_y))

    def update_params(self):
        self.λ = float(self.λ_slider.get())
        self.b = float(self.b_slider.get())

    def toggle_animation(self):
        self.update_params()
        self.running = not self.running
        self.start_btn.config(text="Стоп" if self.running else "Старт")
        self.animate()

    def animate(self):
        if self.running:
            self.points = self.henon_map(self.points)
            self.scat.set_offsets(self.points)
            self.canvas.draw_idle()
            self.after(250, self.animate)

    def reset(self):
        self.running = False
        self.start_btn.config(text="Старт")
        self.points = self.generate_cloud()
        self.scat.set_offsets(self.points)
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = HenonApp()
    app.mainloop()