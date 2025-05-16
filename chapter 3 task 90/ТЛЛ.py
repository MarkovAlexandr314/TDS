import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class MirrorMapApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Гофрированное зеркало")
        self.setup_variables()
        self.create_widgets()
        self.generate_points()

    def setup_variables(self):
        """Инициализация параметров"""
        self.z = tk.DoubleVar(value=1.0)
        self.h = tk.DoubleVar(value=0.5)
        self.grid_size = tk.IntVar(value=20)
        self.iterations = tk.IntVar(value=50)
        self.center_x = tk.DoubleVar(value=np.pi)
        self.center_y = tk.DoubleVar(value=np.pi)
        self.width = tk.DoubleVar(value=2*np.pi)
        self.height = tk.DoubleVar(value=2*np.pi)
        self.points = None
        self.current_iter = 0
        self.anim_running = False
        
        # Строковые переменные для отображения значений
        self.z_value = tk.StringVar()
        self.h_value = tk.StringVar()
        self.update_slider_labels()  # Инициализация начальных значений

    def create_widgets(self):
        """Создание интерфейса"""
        control_frame = ttk.Frame(self.master, padding=10)
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # Параметры с обновленными слайдерами
        self.create_slider(control_frame, "z (интенсивность):", self.z, 0.1, 5.0, self.z_value)
        self.create_slider(control_frame, "h (шаг):", self.h, 0.1, 2.0, self.h_value)

        ttk.Label(control_frame, text="Размер сетки:").pack()
        ttk.Entry(control_frame, textvariable=self.grid_size).pack()

        ttk.Label(control_frame, text="Итерации:").pack()
        ttk.Entry(control_frame, textvariable=self.iterations).pack()

        # Управление
        ttk.Button(control_frame, text="Обновить", command=self.generate_points).pack(pady=5)
        ttk.Button(control_frame, text="Старт", command=self.start_animation).pack(pady=5)
        ttk.Button(control_frame, text="Стоп", command=self.stop_animation).pack(pady=5)

        # График
        self.fig, self.ax = plt.subplots(figsize=(8,8))
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.master)
        self.canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(0, 2*np.pi)
        self.ax.set_xlabel("x")
        self.ax.set_ylabel("y")

    def create_slider(self, parent, label, variable, from_, to_, value_var):
        """Создает слайдер с меткой и отображением значения"""
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.X, pady=2)
        
        ttk.Label(frame, text=label).pack(side=tk.LEFT)
        slider = ttk.Scale(frame, from_=from_, to=to_, variable=variable, 
                          orient=tk.HORIZONTAL, command=lambda v: self.update_slider_labels())
        slider.pack(side=tk.LEFT, expand=True, fill=tk.X)
        ttk.Label(frame, textvariable=value_var, width=5).pack(side=tk.LEFT)

    def update_slider_labels(self, *args):
        """Обновляет отображаемые значения слайдеров"""
        self.z_value.set(f"{self.z.get():.2f}")
        self.h_value.set(f"{self.h.get():.2f}")


    def generate_points(self):
        """Генерация начальных точек"""
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
        self.points = np.column_stack((X.flatten(), Y.flatten()))
        self.current_iter = 0
        self.update_plot()

    def iterate_system(self):
        """Итерация системы"""
        z = self.z.get()
        h = self.h.get()
        
        # Обновление y
        y_new = (self.points[:,1] - z * np.sin(self.points[:,0])) % (2*np.pi)
        # Обновление x
        x_new = (self.points[:,0] + h * np.tan(y_new)) % (2*np.pi)
        
        self.points = np.column_stack((x_new, y_new))
        self.current_iter += 1

    def update_plot(self):
        """Отрисовка точек"""
        self.ax.clear()
        self.ax.scatter(self.points[:,0], self.points[:,1], s=1, c='red')
        self.ax.set_title(f'Итерация: {self.current_iter}')
        self.ax.set_xlim(0, 2*np.pi)
        self.ax.set_ylim(0, 2*np.pi)
        self.canvas.draw()

    def start_animation(self):
        if not self.anim_running:
            self.anim_running = True
            self.animate()

    def stop_animation(self):
        self.anim_running = False

    def animate(self):
        if self.anim_running and self.current_iter < self.iterations.get():
            self.iterate_system()
            self.update_plot()
            self.master.after(50, self.animate)

if __name__ == "__main__":
    root = tk.Tk()
    app = MirrorMapApp(root)
    root.mainloop()