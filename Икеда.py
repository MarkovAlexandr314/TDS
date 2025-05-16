import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class IkedaApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Система Икеды")
        self.geometry("1200x800")
        
        # Параметры системы
        self.A = 0.85
        self.B = 0.9
        self.l = 0.4
        self.running = False
        self.points = self.generate_cloud()
        
        # Создание элементов интерфейса
        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        # Фрейм для управления
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Слайдеры параметров с метками
        self.A_slider, self.A_label = self.create_param_slider(control_frame, "A:", 0.1, 1.5, self.A)
        self.B_slider, self.B_label = self.create_param_slider(control_frame, "B:", 0.1, 1.0, self.B)
        self.l_slider, self.l_label = self.create_param_slider(control_frame, "λ:", 0.1, 1.0, self.l)
        
        # Информация о системе
        self.info_label = ttk.Label(control_frame, text="", wraplength=200)
        self.info_label.pack(pady=10)
        
        # Кнопки управления
        self.btn_frame = ttk.Frame(control_frame)
        self.btn_frame.pack(pady=20)
        
        self.start_btn = ttk.Button(self.btn_frame, text="Старт", command=self.toggle_animation)
        self.start_btn.pack(side=tk.LEFT, padx=5)
        
        self.reset_btn = ttk.Button(self.btn_frame, text="Сброс", command=self.reset)
        self.reset_btn.pack(side=tk.LEFT, padx=5)

    def create_param_slider(self, parent, label, min_val, max_val, init_val):
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        value_label = ttk.Label(frame, width=6)
        value_label.pack(side=tk.RIGHT)
        
        slider = ttk.Scale(frame, from_=min_val, to=max_val, value=init_val,
                          orient=tk.HORIZONTAL,
                          command=lambda v, lbl=value_label: self.update_param(lbl, v))
        slider.pack(side=tk.RIGHT, expand=True, padx=5)
        value_label.config(text=f"{init_val:.2f}")
        return slider, value_label

    def setup_plot(self):
        self.fig = Figure(figsize=(8, 8))
        self.ax = self.fig.add_subplot(111)
        self.ax.set_xlim(-6, 6)
        self.ax.set_ylim(-6, 6)
        self.ax.set_title("Динамика системы Икеды")
        self.scat = self.ax.scatter([], [], s=1, c='blue')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def generate_cloud(self, num=250):
        # Регулярная сетка в комплексной плоскости
        x = np.linspace(-1, 1, num)
        y = np.linspace(-1, 1, num)
        X, Y = np.meshgrid(x, y)
        return X + 1j*Y

    def ikeda_map(self, z):
        # Комплексное отображение Икеды
        return self.A + self.B * z * np.exp(1j*(self.l/(1 + np.abs(z)**2)))

    def update_param(self, label, value):
        label.config(text=f"{float(value):.2f}")
        self.A = float(self.A_slider.get())
        self.B = float(self.B_slider.get())
        self.l = float(self.l_slider.get())
        self.update_system_info()

    def update_system_info(self):
        # Анализ свойств системы
        dissipation = np.abs(self.B)**2  # |det J| = B^2
        system_type = "Консервативная" if np.isclose(dissipation, 1) else "Диссипативная"
        
        info_text = (f"Тип системы: {system_type}\n"
                    f"Коэффициент диссипации: {dissipation:.2f}\n"
                    f"Параметры:\nA={self.A:.2f}, B={self.B:.2f}, λ={self.l:.2f}")
        self.info_label.config(text=info_text)

    def toggle_animation(self):
        self.running = not self.running
        self.start_btn.config(text="Стоп" if self.running else "Старт")
        self.animate()

    def animate(self):
        if self.running:
            # Применяем отображение
            self.points = self.ikeda_map(self.points)
            
            # Визуализация
            self.scat.set_offsets(np.column_stack((np.real(self.points), np.imag(self.points))))
            self.canvas.draw_idle()
            self.after(50, self.animate)

    def reset(self):
        self.running = False
        self.start_btn.config(text="Старт")
        self.points = self.generate_cloud()
        self.scat.set_offsets(np.column_stack((np.real(self.points), np.imag(self.points))))
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = IkedaApp()
    app.mainloop()