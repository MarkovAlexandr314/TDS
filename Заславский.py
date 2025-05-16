import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class ZaslavskyApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Гравитационная машина Заславского")
        self.geometry("1200x800")
        
        # Параметры системы
        self.K = 5.0
        self.gamma = 0.1
        self.omega = 0.618
        self.running = False
        self.points = self.generate_cloud()
        
        # Создание элементов интерфейса
        self.create_widgets()
        self.setup_plot()

    def create_widgets(self):
        # Фрейм для управления
        control_frame = ttk.Frame(self, padding=10)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Слайдеры параметров
        self.K_slider, self.K_label = self.create_param_slider(control_frame, "K:", 0.1, 10.0, self.K)
        self.gamma_slider, self.gamma_label = self.create_param_slider(control_frame, "γ:", 0.0, 1.0, self.gamma)
        self.omega_slider, self.omega_label = self.create_param_slider(control_frame, "Ω:", 0.1, 2.0, self.omega)
        
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
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(-5, 15)
        self.ax.set_title("Фазовое пространство системы Заславского")
        self.ax.set_xlabel("θ")
        self.ax.set_ylabel("p")
        self.scat = self.ax.scatter([], [], s=1, c='blue')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    def generate_cloud(self, num=50):
        theta = np.linspace(0, 2*np.pi, num)
        p = np.linspace(-5, 15, num)
        Theta, P = np.meshgrid(theta, p)
        return np.column_stack((Theta.ravel(), P.ravel()))

    def zaslavsky_map(self, points):
        theta, p = points[:, 0], points[:, 1]
        new_p = (1 - self.gamma)*p + self.K*np.sin(theta) + self.omega
        new_theta = (theta + new_p) % (2*np.pi)
        return np.column_stack((new_theta, new_p))

    def update_param(self, label, value):
        label.config(text=f"{float(value):.2f}")
        self.K = float(self.K_slider.get())
        self.gamma = float(self.gamma_slider.get())
        self.omega = float(self.omega_slider.get())
        self.update_system_info()

    def update_system_info(self):
        system_type = "Консервативная" if self.gamma == 0 else "Диссипативная"
        info_text = (f"Тип системы: {system_type}\n"
                    f"Параметры:\nK={self.K:.2f}, γ={self.gamma:.2f}, Ω={self.omega:.2f}\n"
                    f"Характерные режимы:\n"
                    f"- K < 1: Регулярное движение\n"
                    f"- 1 < K < 5: Стохастический слой\n"
                    f"- K > 5: Развитый хаос")
        self.info_label.config(text=info_text)

    def toggle_animation(self):
        self.running = not self.running
        self.start_btn.config(text="Стоп" if self.running else "Старт")
        self.animate()

    def animate(self):
        if self.running:
            self.points = self.zaslavsky_map(self.points)
            self.scat.set_offsets(self.points)
            self.canvas.draw_idle()
            self.after(50, self.animate)

    def reset(self):
        self.running = False
        self.start_btn.config(text="Старт")
        self.points = self.generate_cloud()
        self.scat.set_offsets(self.points)
        self.canvas.draw_idle()

if __name__ == "__main__":
    app = ZaslavskyApp()
    app.mainloop()